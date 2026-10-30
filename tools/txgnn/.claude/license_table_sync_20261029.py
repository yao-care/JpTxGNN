"""許可證表「狀態」欄跟著許可證事實同步（2026-10-29，許可證排程更新用）。不用 AI、不靠翻譯。

用語從該站自己的頁面學：更新前的頁面＋更新前的 license_facts，統計狀態欄每種寫法對應到哪種狀態
（valid／not_marketed／cancelled），只採「≥90% 對應同一種狀態、出現 ≥2 次」的寫法；每種狀態取最常見的寫法。
更新後：狀態欄的格子是某狀態的已知寫法、但許可證現在是另一種狀態 → 換成新狀態的寫法。
新狀態在該站沒有學到寫法時：用證據包紀錄裡主管機關的原文狀態（pm 2026-10-30：只能用該國官方用語，不跨站借用、不機器翻譯）；
原文也沒有 → 不改、記在 unsynced（排程 summary 列出、開 issue）。
狀態欄＝表頭是 estado／status／statut／状態…的那一欄；許可證號在第一欄。Tw 的許可證表由 tfda 程式產生，不處理。
用法（母目錄或工作目錄）：
  python3 .claude/license_table_sync_20261029.py learn 站 > labels.json   （用目前的 license_facts）
  python3 .claude/license_table_sync_20261029.py apply 站 labels.json [--dry-run]
"""
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
HDR = re.compile(r"^(estado|status|statut|stato|tila|状態|狀態|상태|الحالة|สถานะ|situação|situacao|zulassungsstatus)$", re.I)
SEP = re.compile(r"^\|[\s:|-]+\|\s*$")


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def norm(x):
    return re.sub(r"[\s\-]", "", x).upper()


def facts(site):
    p = BASE / ".claude/cache/license_facts" / f"{site}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def page_facts(fs, stem):
    return fs.get(stem) or fs.get(stem.replace("-", "_")) or fs.get(stem.lower())


def status_cells(lines):
    """產生 (行號, cells, 狀態欄序號)：只在表頭有狀態欄的表格內"""
    col = None
    for i, l in enumerate(lines):
        if not l.startswith("|"):
            col = None
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if i + 1 < len(lines) and SEP.match(lines[i + 1]):
            col = next((k for k, h in enumerate(c) if HDR.match(re.sub(r"\*", "", h).strip())), None)
            continue
        if col is not None and col < len(c) and not SEP.match(l):
            yield i, c, col


def learn(site):
    fs = facts(site)
    m = defaultdict(Counter)
    for f in sorted((BASE / site / "docs/_drugs").glob("*.md")):
        fc = page_facts(fs, f.stem)
        if not fc:
            continue
        lic = {norm(k): v for k, v in (fc.get("licenses") or {}).items()}
        for _, c, col in status_cells(f.read_text(encoding="utf-8", errors="replace").split("\n")):
            s = lic.get(norm(c[0]))
            if s:
                m[c[col]][s] += 1
    # 一種寫法 ≥90% 對應同一種狀態、出現 ≥2 次才採用（容許少數頁落後於事實）
    labels = {txt: cn.most_common(1)[0][0] for txt, cn in m.items()
              if sum(cn.values()) >= 2 and cn.most_common(1)[0][1] / sum(cn.values()) >= 0.9}
    best = {}
    for st in ("valid", "not_marketed", "cancelled"):
        cand = [(sum(m[t].values()), t) for t, s in labels.items() if s == st]
        if cand:
            best[st] = max(cand)[1]
    return {"labels": labels, "preferred": best}


REG_KEYS = ("tfda", "thaifda", "pmda", "npra", "mhra", "tga", "fda")  # 與 reviewer drug_evidence_pack 的順序相同


def reg_block(bundle):
    """證據包裡放本地許可證的區塊（各站欄位名不同：Dk/Nl/Th 用 thaifda、Jp 用 pmda、My 用 npra…）"""
    for k in REG_KEYS:
        v = bundle.get(k)
        if isinstance(v, dict) and v.get("records"):
            return v
    for k in REG_KEYS:
        if isinstance(bundle.get(k), dict):
            return bundle[k]
    return {}


def official_text(site):
    """{許可證號: 主管機關原文狀態}：取自證據包 tfda.records 的 status／registration_status（下載轉換器寫入的官方字樣）"""
    out = {}
    for f in (BASE / site / "data/bundles").glob("*/drug_bundle.json"):
        try:
            recs = reg_block(json.loads(f.read_text(encoding="utf-8"))).get("records", [])
        except Exception:
            continue
        for r in recs:
            k = str(r.get("license_id") or r.get("registration_number") or r.get("reg_no") or "").strip()
            s = str(r.get("status") or r.get("registration_status") or "").strip()
            if k and s:
                out[norm(k)] = s
    return out


def apply(site, lab, dry=False):
    if site == "TwTxGNN":
        return [], []
    fs = facts(site)
    labels, pref = lab["labels"], lab["preferred"]
    off = official_text(site)
    changed, unsynced = [], []
    for f in sorted((BASE / site / "docs/_drugs").glob("*.md")):
        fc = page_facts(fs, f.stem)
        if not fc:
            continue
        lic = {norm(k): v for k, v in (fc.get("licenses") or {}).items()}
        raw = f.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw[:500]
        lines = raw.replace("\r\n", "\n").split("\n")
        ch = False
        for i, c, col in list(status_cells(lines)):
            now = lic.get(norm(c[0]))
            was = labels.get(c[col])
            if not now or not was or was == now:
                continue
            # 本站頁面學到的寫法優先；沒有就用主管機關原文（pm 2026-10-30：只能用該國官方用語，不跨站借、不機器翻譯）
            want = pref.get(now) or off.get(norm(c[0]))
            if not want:
                unsynced.append(f"{f.stem} {c[0]}：{was}→{now}，本站沒有 {now} 的寫法、證據包也沒有官方原文")
                continue
            changed.append((f.stem, f"許可證表 {c[0]} 狀態", c[col], want))
            c[col] = want
            lines[i] = "| " + " | ".join(c) + " |"
            ch = True
        if ch:
            if not dry:
                t = "\n".join(lines)
                f.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
    return changed, unsynced


def sync_market_rows(site, dry=False):
    """只改許可證欄位（2026-10-30，pm 驗收第 2 點：排程不准動 H1、原適應症、description 等其他欄位）：
       概覽表的本站狀態列、既有的張數列（不新增列）。值的寫法與事實層（apply_programmatic）同一套。
       回傳 {頁: [(欄位, 前值, 後值)]}"""
    ap = _load("ap", BASE / ".claude/apply_programmatic_20261023.py")
    ck, mv2 = ap.ck, ap.mv2
    lang = ck.LANG.get(site, "en")
    tl = mv2.T.get(lang) or mv2.T["en"]
    fs = facts(site)
    out = {}
    for f in sorted((BASE / site / "docs/_drugs").glob("*.md")):
        fc = page_facts(fs, f.stem)
        if not fc:
            continue
        raw = f.read_bytes().decode("utf-8")
        if 'http-equiv="refresh"' in raw[:3000] or "layout: id_redirect" in raw[:3000]:
            continue
        crlf = "\r\n" in raw[:500]
        t = raw.replace("\r\n", "\n")
        rows = [r for _, rs, _, _ in ck.tables(t) for r in rs]
        ms, v, n, partial = fc.get("market_status"), fc.get("valid"), fc.get("total"), fc.get("partial")
        ch = []
        st = ck.status_row(site, rows)
        if st and site != "TwTxGNN":
            want = None
            if site == "KrTxGNN":
                want = ck.KR_UNKNOWN
            elif ms == "Marketed":
                want = ck.marketed_text(site, lang, v, n, partial)
            elif ms == "Approved, not marketed":
                want = ck.NOT_MKT.get(lang, ck.NOT_MKT["en"]).format(n=n)
            elif ms == "Cancelled only":
                want = ck.CANCELLED.get(lang, ck.CANCELLED["en"]).format(n=n)
            elif ms == "Not marketed":
                want = ck.not_reg_text(site, lang)
            if want and st[1] != want:
                ch.append((st[0], st[1], want))
        cr = ck.count_row(site, rows)
        if cr and site not in ("TwTxGNN", "KrTxGNN") and n is not None:
            want_c = tl[3].format(n=n) if partial else tl[2].format(n=n, v=v or 0)
            if cr[1] != want_c:
                ch.append((cr[0], cr[1], want_c))
        if not ch:
            continue
        for label, _, value in ch:
            t = re.sub(r"^(\|\s*" + re.escape(label) + r"\s*\|)[^|\n]*(\|)", lambda m: f"{m.group(1)} {value} {m.group(2)}", t, count=1, flags=re.M)
        out[f.stem] = ch
        if not dry:
            f.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
    return out


def drop_excluded_rows(site, dry=False):
    """證據包 tfda.veterinary_records 裡的許可證，從該頁的許可證表刪除整列（pm 2026-10-30：獸用許可不算人用藥）。
    回傳 [(頁, 欄位, 前值, 後值)]"""
    out = []
    for f in sorted((BASE / site / "data/bundles").glob("*/drug_bundle.json")):
        vet = {norm(str(r.get("license_id") or "")) for r in (reg_block(json.loads(f.read_text(encoding="utf-8"))).get("veterinary_records") or [])}
        if not vet:
            continue
        for stem in (f.parent.name, f.parent.name.replace("_", "-")):
            pg = BASE / site / "docs/_drugs" / f"{stem}.md"
            if pg.exists():
                break
        else:
            continue
        raw = pg.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw[:500]
        lines = raw.replace("\r\n", "\n").split("\n")
        keep = []
        for l in lines:
            c = [x.strip() for x in l.strip().strip("|").split("|")] if l.startswith("|") else []
            if c and norm(c[0]) in vet:
                out.append((pg.stem, f"許可證表 {c[0]}（獸用）", l.strip(), "（刪除）"))
                continue
            keep.append(l)
        if len(keep) != len(lines) and not dry:
            t = "\n".join(keep)
            pg.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
    return out


def main(argv):
    if argv[0] == "learn":
        print(json.dumps(learn(argv[1]), ensure_ascii=False, indent=1))
    elif argv[0] == "apply":
        ch, un = apply(argv[1], json.loads(Path(argv[2]).read_text(encoding="utf-8")), "--dry-run" in argv)
        print(f"{argv[1]}：許可證表狀態格改了 {len(ch)} 頁；無法同步 {len(un)} 格")
        for x in un[:50]:
            print("  ", x)


if __name__ == "__main__":
    main(sys.argv[1:])
