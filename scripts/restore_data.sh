#!/bin/bash
# 還原本 repo 沒進 git 的資料（2026-10-29）：data/（許可證原始資料、證據包、藥師報告原稿、預測結果…）與 data/txgnn_cache/。
# 來源是本 repo 的 Release：預設取最新的 data-* tag（排程更新會產生新的 data-YYYYMMDD）。
# --with-kg 另外下載共用知識圖譜與預測模型（只有重跑預測才需要；放在 yao-care/TwTxGNN 的 data-20261016）。
# 用法（repo 根目錄）：bash scripts/restore_data.sh [--tag data-YYYYMMDD] [--with-kg]
set -euo pipefail
cd "$(dirname "$0")/.."
SITE=$(tr -d '[:space:]' < tools/txgnn/SITE)
REPO=$(git remote get-url origin | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')
TAG=""; KG=0
while [ $# -gt 0 ]; do
  case "$1" in --tag) TAG=$2; shift 2 ;; --with-kg) KG=1; shift ;; *) echo "不認得的參數：$1" >&2; exit 1 ;; esac
done
# 最新「建立時間」的 data-* tag；-handoff 是交接時的還原點，只在明確指定 --tag 時使用
[ -z "$TAG" ] && TAG=$(gh release list -R "$REPO" -L 100 --json tagName,createdAt -q '[.[]|select((.tagName|startswith("data-")) and (.tagName|endswith("-handoff")|not))]|sort_by(.createdAt)|last|.tagName')
[ -z "$TAG" ] && { echo "找不到 data-* Release" >&2; exit 1; }
check() { if command -v shasum >/dev/null; then shasum -a 256 -c "$1"; else sha256sum -c "$1"; fi; }
get() {  # $1 repo $2 tag $3 asset 前綴 $4 tar 要去掉的路徑層數
  local d; d=$(mktemp -d)
  gh release download "$2" -R "$1" -D "$d" -p "$3.*"
  (cd "$d" && check "$3.sha256")
  if ls "$d/$3".tar.gz.part-* >/dev/null 2>&1; then cat "$d/$3".tar.gz.part-*; else cat "$d/$3.tar.gz"; fi | tar xzf - --strip-components="$4"  # 大檔分片、小檔（cache）不分片
  rm -rf "$d"; echo "✓ $1 $2 $3"
}
get "$REPO" "$TAG" "$SITE-data" 1          # tar 內是 <站>/data/...，去掉第一層解到本 repo
# 母 repo 快取（舊版證據包備份、Kr 的 MFDS 適應症文字）：本 repo 最新的 cache-* Release，沒有就略過
CTAG=$(gh release list -R "$REPO" -L 100 --json tagName,createdAt -q '[.[]|select(.tagName|startswith("cache-"))]|sort_by(.createdAt)|last|.tagName')
[ -n "$CTAG" ] && get "$REPO" "$CTAG" "$SITE-cache" 1
# data/external 有些站是指向 TwTxGNN 的捷徑（打包時只存捷徑）；斷掉的就從 TwTxGNN 的 shared-external 補實體檔
need=0
for f in disease_vocab.csv drug_disease_relations.csv drugbank_vocab.csv; do
  [ -s "data/external/$f" ] || { rm -f "data/external/$f"; need=1; }   # -s 會跟隨捷徑：不存在、空檔、斷掉的捷徑都算缺
done
if [ $need = 1 ]; then
  mkdir -p data/external
  d=$(mktemp -d); gh release download data-20261016 -R yao-care/TwTxGNN -D "$d" -p "shared-external.*"
  (cd "$d" && check shared-external.sha256) && tar xzf "$d"/shared-external.tar.gz -C data/external && rm -rf "$d"
  echo "✓ data/external 共用檔已補上"
fi
if [ $KG = 1 ]; then
  get yao-care/TwTxGNN data-20261016 shared-kg 1              # TwTxGNN/data/{kg,node,kg_directed,edges}.csv → data/
  [ "$SITE" = TwTxGNN ] && get yao-care/TwTxGNN data-20261016 TwTxGNN-model_ckpt 1
fi
echo "完成：$TAG"
