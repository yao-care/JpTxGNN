#!/usr/bin/env python3
"""公開藥物頁的預測有沒有進搜尋索引與 FHIR（2026-11-19 建；各站 scripts/check_seo_docs.py 的一項）。

2026-11-19 盤點：2026-11-16 用 claude -p 重產報告、重開的 876 頁裡，約 870 頁的 docs/data/search-index.json
indications 是空的（母目錄 .claude/rebuild_search_index.py 解析不到重產報告的表格——分數寫 0.9979 不是 99.79%——
又沒有 fallback 到 front matter predicted_indications；舊索引裡也沒有這些藥，因為 noindex 時不收），SMART 查得到藥、
看不到預測；沒有任何關卡擋。這裡逐頁檢查公開藥物頁（不是轉址頁、noindex、search_exclude）：
  1. front matter predicted_indications 扣掉查核紀錄重審撤回的（站上 src/<套件>/regulatory/withdrawn.py）還有預測，
     search-index.json 裡這個藥（網址 slug）卻不在或 indications 是空的 → 錯誤。
     修法：母目錄 python3 .claude/rebuild_search_index.py <本站>（body 解析不到時改用 front matter predicted_indications，
     分數取證據包，要先還原 data/bundles），再壓回單行。
  2. 同上有預測、front matter 有 drugbank_id，docs/fhir/MedicationKnowledge 卻沒有任何一份對到這頁 → 錯誤。
     對頁規則同 check_seo_docs.py 第 14 項與母目錄 .claude/sync_fhir_levels.py：檔名／id 同名（大小寫、- 與 _ 視為相同）
     → front matter drugbank_id → 去分隔符號同名 → 鹽類／水合物寫法對母藥頁 → docs/_data/fhir_page_map.json；轉址頁跟著轉址。
     修法：從 git 歷史找回本站原本的 MK／CUD，或照本站範本產生（預測＝頁面 predicted_indications），再跑
     母目錄 python3 .claude/sync_fhir_levels.py <本站> --apply。
站上沒有 search-index.json 或 docs/fhir/MedicationKnowledge 的那一項不查。
用法：python3 scripts/check_search_index_coverage.py（在站上；列出缺的，exit 1＝有缺）
      python3 .claude/check_search_index_coverage.py <站…>（在母目錄）
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

SALT_RE = re.compile(r"_(sodium|disodium|potassium|calcium|magnesium|hydrochloride|dihydrochloride|hcl|hydrobromide|phosphate|sulfate|sulphate|"
                     r"maleate|mesylate|mesilate|tartrate|bitartrate|citrate|fumarate|besylate|besilate|bromide|chloride|succinate|"
                     r"monohydrate|dihydrate|trihydrate|hemihydrate|hydrate|anhydrous)$")


def _front(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end >= 0 else ""


def _val(block: str, key: str) -> str:
    m = re.search(rf"^{key}:[ \t]*(.*)$", block, re.M)
    return m.group(1).strip().strip("\"'") if m else ""


def _pages() -> dict:
    out = {}
    for f in sorted((DOCS / "_drugs").glob("*.md")):
        t = f.read_text(encoding="utf-8", errors="replace")
        b = _front(t)
        pm = re.search(r"^permalink:\s*[\"']?/drugs/([^/\"'\s]+)/?[\"']?\s*$", b, re.M)
        tgt = re.search(r'http-equiv="refresh"[^>]*url=(?:https?://[^/"]+)?/drugs/([^/"\s>]+)', t, re.I)
        m = re.search(r"^predicted_indications:\s*(\[.*\])\s*$", b, re.M)
        try:
            preds = [str(x).strip() for x in json.loads(m.group(1)) if str(x).strip()] if m else []
        except ValueError:
            preds = []
        out[f.stem] = {
            "url": pm.group(1) if pm else re.sub(r"[\W_]+", "-", f.stem, flags=re.U).strip("-").lower(),
            "redirect": 'http-equiv="refresh"' in t or _val(b, "layout") == "id_redirect" or bool(_val(b, "redirect_to")),
            "target": tgt.group(1) if tgt else None,
            "hidden": _val(b, "noindex").lower() == "true" or _val(b, "search_exclude").lower() == "true",
            "db": _val(b, "drugbank_id").lower(),
            "preds": preds,
        }
    return out


def _withdrawn():
    for p in sorted(ROOT.glob("src/*/regulatory/withdrawn.py")):
        s = importlib.util.spec_from_file_location(f"withdrawn_{ROOT.name}_cov", p)
        m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m)
        return m, m.load(DOCS / "_data" / "drug_reviews.json")
    return None, {}


def _mk_pages(pages: dict) -> set:
    """有 MedicationKnowledge 對到的藥物頁（轉址後的實際頁）。"""
    by_key, by_url, by_db, by_norm = {}, {}, {}, {}
    for s, p in pages.items():
        for k in {s.lower(), s.lower().replace("-", "_"), s.lower().replace("_", "-")}:
            by_key.setdefault(k, []).append(s)
        by_url.setdefault(p["url"], []).append(s)
        if p["db"] and not p["redirect"]:
            by_db.setdefault(p["db"], []).append(s)
        by_norm.setdefault(re.sub(r"[^a-z0-9]", "", s.lower()), []).append(s)
    mapf = DOCS / "_data" / "fhir_page_map.json"
    pmap = json.loads(mapf.read_text(encoding="utf-8")).get("map", {}) if mapf.exists() else {}

    def one(h, mid=None):
        if len(h) == 1:
            return h[0]
        return next((x for x in h if x == mid), None) if mid else None

    def page(mid: str):
        k = mid.lower()
        hit = None
        for c in (k, k.replace("-", "_"), k.replace("_", "-")):
            if by_key.get(c):
                hit = one(by_key[c], mid)
                break
        if hit is None:
            if re.fullmatch(r"db\d{5}", k):
                hit = one(by_db.get(k) or [])
            else:
                hit = one(by_norm.get(re.sub(r"[^a-z0-9]", "", k)) or [])
                if hit is None:
                    base = re.sub(r"[-\s]", "_", k)
                    while base != (b2 := SALT_RE.sub("", base)):
                        base = b2
                    if base != re.sub(r"[-\s]", "_", k):
                        for c in (base, base.replace("_", "-")):
                            if len(by_key.get(c) or []) == 1:
                                hit = by_key[c][0]
                                break
        if hit is None and mid in pmap and pmap[mid].get("page") in pages:
            hit = pmap[mid]["page"]
        seen = set()
        while hit and pages[hit]["redirect"] and hit not in seen:
            seen.add(hit)
            hit = one([x for x in by_url.get(pages[hit]["target"] or "", []) if x != hit])
        return None if (hit and pages[hit]["redirect"]) else hit

    out = set()
    for f in (DOCS / "fhir" / "MedicationKnowledge").glob("*.json"):
        try:
            r = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for mid in {r.get("id") or f.stem, f.stem}:
            p = page(mid)
            if p:
                out.add(p)
    return out


def check_errors(limit_examples: int = 8) -> list:
    if not (DOCS / "_drugs").is_dir():
        return []
    pages = _pages()
    wd, wtbl = _withdrawn()
    want = {}
    for s, p in pages.items():
        if p["redirect"] or p["hidden"] or not p["preds"]:
            continue
        preds = [x for x in p["preds"] if not (wd and wtbl.get(s) and wd.is_withdrawn(wtbl, s, x))]
        if preds:
            want[s] = preds
    errs = []
    sip = DOCS / "data" / "search-index.json"
    if sip.exists():
        idx = {d.get("slug"): d for d in json.loads(sip.read_text(encoding="utf-8")).get("drugs", [])}
        def _ent(s):  # 索引 slug：網址 slug（母目錄 rebuild_search_index.py）或頁面檔名（Tw 的 generate_search_index.py）
            return next((idx[k] for k in (pages[s]["url"], s, s.replace("_", "-")) if k in idx), {})
        empty = [s for s in want if not _ent(s).get("indications")]
        if empty:
            errs.append(f"公開藥物頁有 predicted_indications、search-index.json 的 indications 卻是空的（或沒有這個藥）{len(empty)} 頁，"
                        f"例：{'、'.join(empty[:limit_examples])}（母目錄跑 python3 .claude/rebuild_search_index.py <本站>，"
                        f"要先還原 data/bundles 取分數；說明見 scripts/check_search_index_coverage.py）")
    if (DOCS / "fhir" / "MedicationKnowledge").is_dir():
        have = _mk_pages(pages)
        # 同一個藥（DrugBank ID）有一份 MK 就算有：MK 檔名／id 就是這個 ID，或同 ID 的另一個公開頁已對到 MK
        # （同 ID 的重複公開頁另由重複頁轉址處理，這裡不重複擋）
        mk_ids = {f.stem.lower() for f in (DOCS / "fhir" / "MedicationKnowledge").glob("*.json")}
        db_have = {pages[s]["db"] for s in have if pages[s]["db"]}
        miss = [s for s in want if pages[s]["db"] and s not in have
                and pages[s]["db"] not in mk_ids and pages[s]["db"] not in db_have]
        if miss:
            ex = "、".join(f"{s}（{pages[s]['db'].upper()}）" for s in miss[:limit_examples])
            errs.append(f"公開藥物頁有預測與 drugbank_id、卻沒有 FHIR MedicationKnowledge 對到 {len(miss)} 頁，"
                        f"例：{ex}"
                        f"（從 git 歷史找回或照本站範本產生，再跑母目錄 .claude/sync_fhir_levels.py <本站> --apply；說明見 scripts/check_search_index_coverage.py）")
    return errs


def _main(argv) -> int:
    global ROOT, DOCS
    sites = [a for a in argv if not a.startswith("-")]
    if not sites:  # 在站上跑：scripts/check_search_index_coverage.py
        sites = [None]
    bad = 0
    for site in sites:
        if site:  # 在母目錄跑：.claude/check_search_index_coverage.py <站…>
            ROOT = (Path(__file__).resolve().parent.parent / site).resolve()
            DOCS = ROOT / "docs"
        e = check_errors(limit_examples=10**6)
        tag = f"{ROOT.name}: " if site else ""
        for x in e:
            print(f"✗ {tag}{x}")
        if not e:
            print(f"✓ {tag}公開藥物頁的預測都在搜尋索引裡、有 drugbank_id 的都有 FHIR MedicationKnowledge")
        bad += bool(e)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
