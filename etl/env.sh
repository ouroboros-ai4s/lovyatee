#!/usr/bin/env bash
# source etl/env.sh — 激活 etl 环境；所有临时文件与缓存落在 /data_new/ywy
export ETL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source /data_new/ywy/envs/etl/bin/activate
export PATH="/data_new/ywy/tools/hmmer/usr/bin:$PATH"
export PYTHONPATH="$ETL_ROOT${PYTHONPATH:+:$PYTHONPATH}"
export TMPDIR=/data_new/ywy/tmp
export UV_CACHE_DIR=/data_new/ywy/cache/uv
export XDG_CACHE_HOME=/data_new/ywy/cache/xdg
export RCSB_CACHE=/data_new/ywy/cache/rcsb
export ETL_PROXY=http://127.0.0.1:17890
mkdir -p "$TMPDIR" "$UV_CACHE_DIR" "$XDG_CACHE_HOME" "$RCSB_CACHE"
