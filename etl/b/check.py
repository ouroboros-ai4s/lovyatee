"""单个 SRC 的完成判据 1–6：`python -m etl.b.check SRC_R76`。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import duckdb
import pyarrow.parquet as pq

from etl.core.merge import PAIR_SCHEMA, merge

OUT = Path("/data_new/wyy".replace("wyy", "wyy"))


def _p(src_dir: Path, name: str) -> Path:
    return src_dir / name


def check(src: str, out_root: Path = Path("/data_new/ywy/etl_out")) -> dict:
    d = out_root / src
    result = {}
    rec = json.loads((d / "reconcile.json").read_text())
    result["reconcile"] = rec

    raw = pq.read_table(d / "raw_ab.parquet").num_rows
    rej = pq.read_table(d / "reject_log.parquet").to_pylist()
    adapt_rej = sum(1 for r in rej if r["stage"] == "adapt")
    result["check1_adapt"] = {"raw_records": raw,
                              "expected": rec["records"] + adapt_rej,
                              "ok": raw == rec["records"] + adapt_rej}

    ab = pq.read_table(d / "ab_entity.parquet").to_pylist()
    ag = pq.read_table(d / "ag_entity.parquet").to_pylist()
    result["check2_ab"] = {"keys": len(ab),
                           "ok": len(ab) == sum(1 for r in ab if not r["reason_code"])
                           + sum(1 for r in ab if r["reason_code"])}
    result["check2_ag"] = {"keys": len(ag),
                           "ok": len(ag) == sum(1 for r in ag if not r["reason_code"])
                           + sum(1 for r in ag if r["reason_code"])}

    pair = pq.read_table(d / "pair.parquet", schema=PAIR_SCHEMA)
    asm_rej = sum(1 for r in rej if r["stage"] == "assemble")
    result["check3_assemble"] = {"records": rec["records"], "pairs": pair.num_rows,
                                 "rejects": asm_rej,
                                 "ok": rec["records"] == pair.num_rows + asm_rej}

    mg = out_root / src / "merge_check"
    rep = merge(str(d / "pair.parquet"), mg, reject_glob=str(d / "reject_log.parquet"),
                shards=1, qa_per_stratum=10)
    n_obs = sum(len(o) for o in pair.column("obs").to_pylist())
    con = duckdb.connect()
    got = con.execute('select sum(len(affinity)) from read_parquet(?)',
                      [str(mg / "3a" / "*.parquet")]).fetchone()[0]
    result["check4_merge"] = {"n_pairs": rep.n_pairs, "n_3a": rep.n_3a,
                              "n_obs_pairs": n_obs, "sum_affinity": got,
                              "ok": got == n_obs and rep.n_obs == n_obs,
                              "merged": rep.n_pairs - rep.n_3a}

    reasons = {}
    for r in rej:
        reasons[r["reason_code"]] = reasons.get(r["reason_code"], 0) + 1
    total = max(1, rec["records"] + adapt_rej)
    result["check5_reasons"] = {k: {"n": v, "share": round(v / total, 4)}
                                for k, v in sorted(reasons.items(), key=lambda t: -t[1])}
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    args = ap.parse_args(argv)
    print(json.dumps(check(args.src), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
