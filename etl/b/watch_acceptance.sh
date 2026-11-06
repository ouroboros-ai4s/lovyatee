#!/usr/bin/env bash
# 等验收脚本结束，然后提交并推送分支；全程在 host 上。
set -u
cd /data_new/ywy/LOVYATEE
source etl/env.sh
LOG=/data_new/ywy/etl_out/acceptance.log
while ! grep -q "^=== done" "$LOG" 2>/dev/null; do
  if ! pgrep -f "etl/b/acceptance.sh" >/dev/null; then
    echo "acceptance.sh exited without done marker" >> /data_new/ywy/etl_out/watch.log
    break
  fi
  sleep 60
done
echo "=== acceptance finished $(date -Is)" >> /data_new/ywy/etl_out/watch.log
git add -A etl
git -c user.name="Pthahnix" -c user.email="pthahnix@users.noreply.github.com" \
    commit -q -m "feat(etl-b): final merge, acceptance and reproducibility check

Co-Authored-By: Claude Code <noreply@anthropic.com>" >> /data_new/ywy/etl_out/watch.log 2>&1
git push -u origin etl-b-layer >> /data_new/ywy/etl_out/watch.log 2>&1
echo "=== push rc=$? $(date -Is)" >> /data_new/ywy/etl_out/watch.log
