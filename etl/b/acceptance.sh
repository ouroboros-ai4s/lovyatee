#!/usr/bin/env bash
# 最终验收：单源 check -> 全局 merge -> 复现复跑 -> 抽取核对。全部在 host 上跑。
set -u
cd /data_new/ywy/LOVYATEE
source etl/env.sh
OUT=/data_new/ywy/etl_out
LOG=$OUT/acceptance.log
exec > >(tee -a "$LOG") 2>&1
echo "=== start $(date -Is) ==="

echo "--- 1. single-SRC checks ---"
for s in R03 R08 R09 R10 R11 R12 R13 R14 R15 R16 R23 R50 R74 R75 R76 R77 R78 R79 R80; do
  python -B -m etl.b.check SRC_${s} > "$OUT/SRC_${s}/check.json" 2>"$OUT/SRC_${s}/check.err" \
    && echo "$s check ok" || echo "$s check FAILED"
done

echo "--- 2. global merge ---"
python -B -m etl.b.final_merge --out "$OUT/final" --qa-per-stratum 50 --shards 16

echo "--- 3. reproducibility (same input, second run) ---"
python -B -m etl.b.final_merge --out "$OUT/final_rerun" --qa-per-stratum 50 --shards 16
python -B - <<'PY'
import hashlib
from pathlib import Path
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
a, b = Path("/data_new/ywy/etl_out/final"), Path("/data_new/ywy/etl_out/final_rerun")
same = True
for f in sorted((a / "3a").glob("*.parquet")):
    g = b / "3a" / f.name
    if not g.exists() or h(f) != h(g):
        print("DIFF", f.name); same = False
print("3a byte-identical:", same)
print("manifest identical:", (a / "manifest.json").read_bytes() == (b / "manifest.json").read_bytes())
PY

echo "--- 4. qa_sample spot check ---"
python -B - <<'PY'
import json, random
from pathlib import Path
import pyarrow.parquet as pq
from etl.core.lineage import split
out = Path("/data_new/ywy/etl_out/final")
qa = pq.read_table(out / "qa_sample.parquet").to_pylist()
three = {r["3A_ID"]: r for r in pq.read_table(out / "3a").to_pylist()}
random.seed(0)
print("qa rows", len(qa), "strata", sorted({q["stratum"] for q in qa}))
for stratum in sorted({q["stratum"] for q in qa}):
    for q in random.sample([x for x in qa if x["stratum"] == stratum], min(3, sum(1 for x in qa if x["stratum"] == stratum))):
        r = three.get(q["3A_ID"])
        if not r:
            print(stratum, q["3A_ID"][:10], "MISSING"); continue
        loc = split(r["affinity"][0]["lineage"][0])[:3] if r["affinity"] else []
        print(stratum, q["3A_ID"][:10], "vh", len(r["antibody"]["vh_sequence"] or ""),
              "vl", len(r["antibody"]["vl_sequence"] or ""),
              "ag", [len(s) for s in r["antigen"]["sequence"]],
              "obs", len(r["affinity"]), loc)
PY

echo "--- 5. reject shares per SRC ---"
python -B - <<'PY'
import json
from pathlib import Path
for d in sorted(Path("/data_new/ywy/etl_out").glob("SRC_R*")):
    f = d / "reconcile.json"
    if not f.exists():
        continue
    r = json.loads(f.read_text())
    total = max(1, r.get("covered_rows") or r.get("source_rows") or r["records"])
    sh = {k: round(v / total, 4) for k, v in r["reasons"].items()}
    over = {k: v for k, v in sh.items() if v > 0.5}
    print(d.name, "pairs", r["pairs"], "3a", r["distinct_3a"], "shares", sh,
          ("OVER-HALF " + str(over)) if over else "")
PY

echo "=== done $(date -Is) ==="
