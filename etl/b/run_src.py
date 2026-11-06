"""跑一个 SRC：`python -m etl.b.run_src R76 [--workers 32]`。"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from pathlib import Path

from etl.b import entities, pipeline


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--out", default=str(pipeline.DEFAULT_OUT))
    ap.add_argument("--adapt-only", action="store_true")
    args = ap.parse_args(argv)

    adapter = importlib.import_module("etl.adapters." + args.src.lower())
    t0 = time.time()
    records, rejects = adapter.adapt()
    # records 可能是生成器（R50 的 94 万行）；rejects 由 adapter 在流式产出后填满
    if hasattr(records, "__len__"):
        print(f"adapt: {len(records)} records, {len(rejects)} rejects "
              f"({time.time() - t0:.1f}s)", flush=True)
    if args.adapt_only:
        if not hasattr(records, "__len__"):
            records = list(records)
        print(f"adapt-only: {len(records)} records, {len(rejects)} rejects",
              flush=True)
        return 0

    name = getattr(adapter, "SRC", "SRC_" + args.src.upper())
    decisions = sorted(Path("etl/decisions").glob(f"*{args.src.upper()}*.yaml"))
    runner = (pipeline.run_sharded if getattr(adapter, "SHARDED", False)
              else pipeline.run)
    summary = runner(name, records, rejects, entities.ab_entity, entities.ag_entity,
                     out_root=Path(args.out), workers=args.workers,
                     decisions=decisions,
                     source_rows=getattr(adapter, "SOURCE_ROWS", None))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
