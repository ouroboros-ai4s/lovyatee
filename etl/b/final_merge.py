"""全局 merge：`python -m etl.b.final_merge [--out DIR] [--rerun]`。

20 个 SRC 的 pair + reject_log 合并成 3a shards、stats、qa_sample、manifest。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from etl.core.merge import merge

OUT_ROOT = Path("/data_new/ywy/etl_out")
SRCS = ["SRC_R03", "SRC_R08", "SRC_R09", "SRC_R10", "SRC_R11", "SRC_R12",
        "SRC_R13", "SRC_R14", "SRC_R15", "SRC_R16", "SRC_R20", "SRC_R23",
        "SRC_R50", "SRC_R74", "SRC_R75", "SRC_R76", "SRC_R77", "SRC_R78",
        "SRC_R79", "SRC_R80"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT_ROOT / "final"))
    ap.add_argument("--qa-per-stratum", type=int, default=50)
    ap.add_argument("--shards", type=int, default=16)
    args = ap.parse_args(argv)

    pairs, rejs, missing = [], [], []
    for src in SRCS:
        p = OUT_ROOT / src / "pair.parquet"
        r = OUT_ROOT / src / "reject_log.parquet"
        if p.exists():
            pairs.append(str(p))
            if r.exists():
                rejs.append(str(r))
        elif src != "SRC_R20":       # R20 是资源适配器，不产 pair
            missing.append(src)
    if missing:
        print("missing pairs:", missing, file=sys.stderr)
        return 1

    decisions = sorted(Path("etl/decisions").glob("*.yaml"))
    rep = merge(pairs, Path(args.out), reject_glob=rejs, shards=args.shards,
                qa_seed=0, qa_per_stratum=args.qa_per_stratum,
                decision_files=decisions)
    print(json.dumps({"n_pairs": rep.n_pairs, "n_3a": rep.n_3a,
                      "n_obs": rep.n_obs, "n_rejected": rep.n_rejected},
                     indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
