"""结构引用 → 链记录。gemmi 解析 PDB/mmCIF；RCSB 缺失时经 ETL_PROXY 下载并缓存。"""
import hashlib
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

import gemmi

from etl.core.lineage import kv, step
from etl.core.resolve import LEVELS, Candidate, resolve

RCSB_FILES = "https://files.rcsb.org/download/%s.cif"
RCSB_REMOVED = "https://data.rcsb.org/rest/v1/holdings/removed/%s"
PICK_LEVELS = LEVELS[:4]
_AA = gemmi.find_tabulated_residue


class StructureNotFound(Exception):
    """RCSB 无此条目，或撤销后没有唯一替代。"""


@dataclass(frozen=True)
class ChainRecord:
    chain_id: str
    entity_id: str
    is_protein: bool
    full_seq: str
    observed_seq: str
    index_of: Mapping[tuple[int, str], int]

    def observed_segments(self) -> tuple[str, ...]:
        return _segments(self.full_seq, tuple(self.index_of.values()))

    def consistent_with(self, seq: str) -> bool:
        return all(seg in seq for seg in self.observed_segments())


def _segments(full: str, positions: Sequence[int]) -> tuple[str, ...]:
    """已观察残基按 full_seq 下标切连续片段；下标不连续处断开。"""
    if not positions:
        return ()
    out, start, prev = [], positions[0], positions[0]
    for pos in positions[1:]:
        if pos != prev + 1:
            out.append(full[start:prev + 1])
            start = pos
        prev = pos
    out.append(full[start:prev + 1])
    return tuple(out)


@dataclass(frozen=True)
class Structure:
    structure_id: str
    requested_id: str
    file: Path
    sha256: str
    chains: Mapping[str, ChainRecord]
    lineage: tuple[str, ...]
    replaced_from: str | None = None


def _one(residue_name: str) -> str:
    code = _AA(residue_name).one_letter_code
    return code.upper() if code and code.isalpha() else "X"


def _chain_record(st: gemmi.Structure, chain: gemmi.Chain) -> ChainRecord:
    polymer = chain.get_polymer()
    entity = st.get_entity_of(polymer)
    residues = list(polymer)
    observed = [_one(r.name) for r in residues]
    is_protein = bool(residues) and all(_AA(r.name).is_amino_acid() for r in residues)
    full, index_of = "", {}
    if entity is not None and entity.full_sequence:
        full = "".join(_one(n) for n in entity.full_sequence)
        if full == "".join(observed):
            index_of = {(r.seqid.num, r.seqid.icode.strip()): i for i, r in enumerate(residues)}
        else:
            result = gemmi.align_sequence_to_polymer(list(entity.full_sequence), polymer,
                                                     entity.polymer_type)
            hit = 0
            for pos, flag in enumerate(result.match_string):
                if flag == "|":
                    r = residues[hit]
                    index_of[(r.seqid.num, r.seqid.icode.strip())] = pos
                    hit += 1
    if not full:
        full = "".join(observed)
        index_of = {(r.seqid.num, r.seqid.icode.strip()): i for i, r in enumerate(residues)}
    return ChainRecord(chain.name, entity.name if entity else "", is_protein,
                       full, "".join(observed), index_of)


def _parse(path: Path, structure_id: str, requested_id: str | None = None) -> Structure:
    st = gemmi.read_structure(str(path))
    st.setup_entities()
    chains = {c.name: _chain_record(st, c) for c in st[0]} if len(st) else {}
    return Structure(structure_id, requested_id or structure_id, path,
                     hashlib.sha256(path.read_bytes()).hexdigest(), chains,
                     (step("structure_open", kv("structure_id", structure_id)),))


def _ssl_context() -> ssl.SSLContext:
    # ponytail: 这条线路对含 ML-KEM 的 ClientHello 不友好，限定 X25519 + http/1.1
    ctx = ssl.create_default_context()
    ctx.set_ecdh_curve("X25519")
    ctx.set_alpn_protocols(["http/1.1"])
    return ctx


def _fetch(url: str, proxy: str | None, attempts: int = 4) -> bytes | None:
    """返回响应体；404 返回 None；其他错误重试后抛 OSError（乱序的握手失败很常见）。"""
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"https": proxy} if proxy else {}),
        urllib.request.HTTPSHandler(context=_ssl_context()))
    last = None
    for n in range(attempts):
        try:
            with opener.open(url, timeout=90) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            last = exc
        except Exception as exc:
            last = exc
        time.sleep(2 * (n + 1))
    raise OSError("fetch failed: %s: %s" % (url, last))


def _replacement(pdb_id: str, proxy: str | None) -> str | None:
    body = _fetch(RCSB_REMOVED % pdb_id, proxy)
    if not body:
        return None
    codes = json.loads(body).get("rcsb_repository_holdings_removed", {}).get(
        "id_codes_replaced_by") or []
    return codes[0].upper() if len(codes) == 1 else None


def _download(pdb_id: str, cache: Path, proxy: str | None) -> Path | None:
    cached = cache / (pdb_id + ".cif")
    if cached.exists():
        return cached
    body = _fetch(RCSB_FILES % pdb_id, proxy)
    if body is None:
        return None
    cache.mkdir(parents=True, exist_ok=True)
    tmp = cached.with_suffix(".cif.tmp")
    tmp.write_bytes(body)
    os.replace(tmp, cached)
    return cached


def open_structure(ref: str | Path, cache_dir: Path | None = None) -> Structure:
    """ref 是现有文件则直接解析；否则当 PDB ID，先查缓存再经 ETL_PROXY 下载。"""
    path = Path(ref)
    if path.exists():
        return _parse(path, path.stem.split(".")[0])
    cache = Path(cache_dir or os.environ.get("RCSB_CACHE", "/data_new/ywy/cache/rcsb"))
    proxy = os.environ.get("ETL_PROXY")
    requested = path.name.strip().upper()
    replaced_from = None
    cached = cache / (requested + ".cif")
    if not cached.exists():
        # RCSB 仍会返回已撤销条目，所以先查替代关系，再决定下载哪个 ID
        structure_id = _replacement(requested, proxy)
        if structure_id:
            replaced_from, requested = requested, structure_id
    cached = _download(requested, cache, proxy)
    if cached is None:
        if replaced_from:
            raise StructureNotFound(requested)
        structure_id = _replacement(requested, proxy)
        if structure_id is None:
            raise StructureNotFound(requested)
        cached = _download(structure_id, cache, proxy)
        if cached is None:
            raise StructureNotFound(structure_id)
        replaced_from, requested = requested, structure_id
    structure = _parse(cached, cached.stem, requested)
    if replaced_from:
        line = step("structure_open", kv("replaced_from", replaced_from),
                    kv("structure_id", cached.stem))
        return Structure(requested, structure.requested_id, structure.file, structure.sha256,
                         structure.chains, (line,), replaced_from)
    return structure


def pick_sequence(rec: ChainRecord, source: str | None = None,
                  fasta: str | None = None) -> tuple[str | None, tuple[str, ...]]:
    """按 source_native > fasta > structure_canonical > structure_observed 择优。"""
    mapping = (("source_native", source), ("source_fasta_or_rebuilt", fasta),
               ("structure_canonical", rec.full_seq), ("structure_observed", rec.observed_seq))
    cands = tuple(Candidate(level, seq) for level, seq in mapping if seq)
    r = resolve(cands, PICK_LEVELS, on_tie="pick_top")
    if r.selected is None:
        return None, ()
    if r.selected.source in ("structure_canonical", "structure_observed"):
        frags = [f for f in r.lineage_frags() if not f.startswith("candidates=")]
        return str(r.selected.value), (step("structure_recover", *frags),)
    return str(r.selected.value), ()
