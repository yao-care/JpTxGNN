#!/bin/bash
# 組出 TxGNN 工具鏈的工作目錄（2026-10-29）：<ws>/.claude＝tools/txgnn/.claude 的複本，<ws>/<站>＝本 repo（symlink）。
# 工具鏈（事實層、checker、許可證更新…）以 <ws> 為母目錄原封不動地跑，只看得到本站。
# 快取（license_facts 會當場重算；bundle_backup／kr_mfds_ee 由 scripts/restore_data.sh 放進 data/txgnn_cache/）一併接上。
# 用法：WS=$(bash scripts/txgnn_ws.sh [工作目錄])；之後在 $WS 跑 python3 .claude/<腳本> <站>
set -euo pipefail
REPO=$(cd "$(dirname "$0")/.." && pwd)
SITE=$(tr -d '[:space:]' < "$REPO/tools/txgnn/SITE")
WS=${1:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/txgnn-ws-$SITE}
mkdir -p "$WS"
rm -rf "$WS/.claude"
cp -R "$REPO/tools/txgnn/.claude" "$WS/.claude"
ln -sfn "$REPO" "$WS/$SITE"
if [ -d "$REPO/data/txgnn_cache" ]; then
  for d in "$REPO"/data/txgnn_cache/*; do [ -e "$d" ] && ln -sfn "$d" "$WS/.claude/cache/$(basename "$d")"; done
fi
echo "$WS"
