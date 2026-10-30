"""事實層之後剩下的頁：依 checker 錯誤型態用程式修（2026-10-29，不用 AI）。通用規則，不寫死頁面；改後多出新錯就退回。

  1. 快速總覽表裡多塞的候選列（已移除預測、百分比、KG 預測）→ 整列刪
  2. 市場狀態 Unknown（部分紀錄）卻寫上市中（M2）→ 狀態格改「本地資料未記載」
  3. 表格等級格 L1–L4 但證據包沒有直接研究（P4）→ 該格改 L5
  4. 表格裡把 KG 當預測來源的格子（P5「KG |」）→ 「—」
  5. 預測表裡病名本身就是已排除預測的列（P3 已排除…出現在預測列）→ 整列刪
  6. 已知用途頁核准區列了出處是 kg／related 的病名（K1）→ 該列刪；標題含知識圖譜的小節（P5）→ 整節刪
  7. Tw 缺本站狀態列（M1）→ 依 license_facts 補
用法（母目錄）：python3 .claude/fix_residual_20261029.py [--apply] --pages site:page,...
"""
import importlib.util
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


sys_argv, sys.argv = sys.argv, ["x"]
fl = _load("fl", BASE / ".claude/factlayer_20261028.py")
sys.argv = sys_argv
ck, dm = fl.ck, fl.dm
SEP = re.compile(r"^\|[\s:|-]+\|\s*$")


def cells(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


def fix(site, page, text, cls, errs):
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if 'id="pharmacist"' in l), 0)
    ov = set(fl.overview_rows(lines, start))
    b = ck.amf.load_bundle(BASE / site, page) or {}
    d = b.get("drug") or {}
    kept = ck.kf.kept_predictions(BASE / site, b) if cls not in ("no_pred_keep", "no_pred_noindex") else []
    keep_rx = [rx for k in kept for rx in ck.name_regexes(site, k)]
    top = [p["disease_name"] for p in d.get("predicted_indications") or [] if (p.get("txgnn_score") or 0) >= ck.kf.SCORE_MIN][:10]
    excluded = [x for x in top if ck.norm_name(x) not in {ck.norm_name(k) for k in kept}]
    drop, codes = set(), {e[0] for e in errs}
    msgs = [m for _, m in errs]
    for i, l in enumerate(lines):
        if not l.startswith("|") or SEP.match(l):
            continue
        c = cells(l)
        # 1／5：已移除或已排除的預測列
        if any("仍在正文" in m and m.split("：", 1)[-1].strip()[:25] in l for m in msgs) and i in ov and not ck.PRED_ROW.search(c[0]) and not dm.PRED_LABEL.search(c[0]):
            drop.add(i); continue
        if i in ov and (fl.PCT_ANY.search(ck.norm_digits(l)) or fl.KG_PRED_ROW.search(c[0]) or re.search(r"knowledge.?g", l, re.I)) \
                and not (ck.PRED_ROW.search(c[0]) or dm.PRED_LABEL.search(c[0]) or fl.SCORE_LABEL.search(c[0]) or ck.ORIG_ROW.search(c[0])):
            drop.add(i); continue
        if "P3" in codes and i not in ov and ck.score_tokens(l) and len(c) >= 2:
            name_cell = next((x for x in c if re.search(r"[A-Za-zÀ-ɏ؀-ۿ฀-๿぀-鿿]", x) and not ck.score_tokens(x)), "")
            if any(ck.norm_name(name_cell) == ck.norm_name(x) for x in excluded):  # 病名欄就是已排除預測（名稱與 kept 部分重疊也一樣）
                drop.add(i); continue
            if any(rx.search(name_cell) for x in excluded for rx in ck.name_regexes(site, x)) and \
                    not any(rx.fullmatch(name_cell) or rx.search(name_cell) and len(name_cell) < 60 for rx in keep_rx):
                drop.add(i); continue
        # 4：KG 當來源的格子
        if "P5" in codes and any(x in ("KG", "KG)") or re.fullmatch(r"\(?KG\)?", x) for x in c):
            lines[i] = "| " + " | ".join("—" if re.fullmatch(r"\(?KG\)?", x) else x for x in c) + " |"
        # 3：P4 等級格
        if "P4" in codes and i not in ov:
            for m in msgs:
                mm = re.search(r"(L[1-4]) 但證據包沒有直接研究「(.+?)」", m)
                if mm and any(rx.search(l) for rx in ck.name_regexes(site, mm.group(2))):
                    lines[i] = re.sub(r"(?<![A-Za-z0-9])" + mm.group(1) + r"(?![0-9])", "L5", lines[i])
    # 2：M2 狀態格
    if "M2" in codes:
        st = ck.status_row(site, [cells(lines[i]) for i in ov])
        if st:
            i = next(i for i in ov if cells(lines[i])[0] == st[0])
            lines[i] = f"| {st[0]} | {fl.NOT_RECORDED[fl.lang_of(site)]} |"
    # 6：已知用途頁 K1、知識圖譜小節
    if cls == "known_use" or "K1" in codes:
        k1 = [re.search(r"「(.+?)」出處是", m).group(1) for m in msgs if "出處是" in m]
        zone_approved = False
        for i, l in enumerate(lines):
            if l.startswith("###"):
                zone_approved = not (ck.KG_WORD.search(l) or re.search(r"categor|類別|同類|カテゴリ|범주|Kategori|catégorie|categoría|luokka|kategori|فئة|หมวด", l, re.I))
                continue
            if zone_approved and l.startswith("|") and any(rx.search(l) for x in k1 for rx in ck.name_regexes(site, x)):
                drop.add(i)
    if "P5" in codes:
        for i, l in enumerate(lines):
            if l.startswith("###") and any(m.strip()[:20] in l for m in msgs):
                j = i + 1
                while j < len(lines) and not lines[j].startswith(("## ", "### ")):
                    j += 1
                drop |= set(range(i, j))
    out = [l for i, l in enumerate(lines) if i not in drop]
    text = "\n".join(out)
    # 3b：P4 落在主預測（快速總覽等級列／頁首）→ 全頁等級改 L5（front matter、parent、頁首、總覽等級列）
    if "P4" in codes:
        pmap = fl.ap.parent_map(site)
        text = re.sub(r"^evidence_level:\s*L[1-4]\s*$", "evidence_level: L5", text, count=1, flags=re.M)
        if "L5" in pmap:
            text = re.sub(r"^parent:\s*.+$", f"parent: {pmap['L5']}", text, count=1, flags=re.M)
        text = fl.ap.HEAD_L.sub(lambda m: f"{m.group(1)}L5{m.group(3)}", text, count=1)
        ls = text.split("\n")
        for i in fl.overview_rows(ls, start):
            c = cells(ls[i])
            if len(c) >= 2 and ck.LEVEL_ROW.search(c[0]):
                ls[i] = re.sub(r"(?<![A-Za-z0-9])L[1-4](?![0-9])", "L5", ls[i])
        text = "\n".join(ls)
    # 7：Tw 缺狀態列
    if site == "TwTxGNN" and any("找不到本站狀態列" in m for m in msgs):
        fc = ck.facts(site).get(page) or {}
        val = fl.status_value("HkTxGNN", fc) if fc else None  # 中文狀態句（與 Hk 同一套用語）
        ls = text.split("\n")
        ovl = fl.overview_rows(ls, start)
        at = next((i for i in ovl if ck.ORIG_ROW.search(cells(ls[i])[0])), ovl[0] if ovl else None)
        if at is not None and val:
            ls.insert(at + 1, f"| 台灣上市 | {val} |")
            text = "\n".join(ls)
    return text


def main(argv):
    apply_ = "--apply" in argv
    pages = [tuple(x.split(":", 1)) for x in argv[argv.index("--pages") + 1].split(",") if x]
    cl = ck.classification()
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    n = fixed = 0
    for s, p in pages:
        f = BASE / s / "docs/_drugs" / f"{p}.md"
        cls = cl.get((s, p), "keep")
        raw = f.read_bytes().decode("utf-8"); crlf = "\r\n" in raw[:500]; t0 = raw.replace("\r\n", "\n")
        errs = [e for e in ck.check_page(s, f, cls, False) if e[0] != "P7"]
        if not errs:
            continue
        n += 1
        t2 = fix(s, p, t0, cls, errs)
        tmp = BASE / ".claude/audit_20261016/fix_residual" / s / f.name
        tmp.parent.mkdir(parents=True, exist_ok=True); tmp.write_text(t2, encoding="utf-8")
        after = [e for e in ck.check_page(s, tmp, cls, False) if e[0] != "P7"]
        if {e[0] for e in after} - {e[0] for e in errs} or len(after) > len(errs):
            print(f"✗退回 {s}:{p} {sorted({e[0] for e in errs})}→{sorted({e[0] for e in after})}"); continue
        if t2 != t0:
            t2 = re.sub(r"^last_modified_at:.*$", f"last_modified_at: {today}", t2, count=1, flags=re.M)
            if apply_:
                f.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
        fixed += not after
        print(f"{'✓' if not after else '…'} {s}:{p} {sorted({e[0] for e in errs})}→{sorted({e[0] for e in after})}")
    print(f"處理 {n} 頁，歸零 {fixed} 頁")


if __name__ == "__main__":
    main(sys.argv[1:])
