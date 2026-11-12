"""查核紀錄裡重審撤回（verdict=withdraw）的預測（2026-11-12 建，比照 TwTxGNN／UsTxGNN 的 withdrawn.py）。

頁面上的模型預測原文依站方規則不刪不改寫，但撤回的預測不再對外當成「預測」發布：
證據監測（scripts/extract_drug_list.py）、搜尋索引（母目錄 .claude/rebuild_search_index.py、本站 scripts/generate_search_index.py）、
FHIR（母目錄 .claude/sync_fhir_levels.py、本站 scripts/generate_fhir_resources.py）都用這裡的名單排除；gate 也檢查。名單以 docs/_data/drug_reviews.json 為準：
rereview_result 且 verdict=withdraw 的紀錄，取 known_use_exclusion[].predicted（已核准用途撤回）
或 withdrawn_predictions（其他撤回），兩者都是 front matter predicted_indications 的原字串。
被標 resolved_by_regeneration／withdrawn 的紀錄不算。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REVIEWS = Path(__file__).resolve().parents[3] / "docs" / "_data" / "drug_reviews.json"
INACTIVE = ("resolved_by_regeneration", "withdrawn")


def load(path: Path | None = None) -> dict[str, set[str]]:
    """{頁面 slug（檔名去 .md）: {撤回的預測名稱（小寫）}}。"""
    path = path or REVIEWS
    if not path.exists():
        return {}
    out: dict[str, set[str]] = {}
    for r in json.loads(path.read_text(encoding="utf-8")).get("records", []):
        if r.get("action") != "rereview_result" or r.get("verdict") != "withdraw" or r.get("status") in INACTIVE:
            continue
        names = [e.get("predicted") for e in r.get("known_use_exclusion") or []]
        names += r.get("withdrawn_predictions") or []
        slug = r["file"][:-3] if r["file"].endswith(".md") else r["file"]
        out.setdefault(slug, set()).update(n.strip().lower() for n in names if n and n.strip())
    return out


def _paren_contents(s: str) -> list[str]:
    """字串裡每一組（可巢狀的）括號內容；全形括號視同半形。"""
    s = s.replace("（", "(").replace("）", ")")
    out, stack = [], []
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")" and stack:
            out.append(s[stack.pop() + 1:i])
    return out


def name_candidates(name: str) -> set[str]:
    """索引／FHIR 的適應症名稱可能是英文原名，或「當地名 (English)」；全部候選轉小寫。"""
    name = (name or "").strip()
    return {c.strip().lower() for c in [name, *_paren_contents(name)] if c.strip()}


def is_withdrawn(table: dict[str, set[str]], slug: str, name: str) -> bool:
    gone = table.get(slug)
    return bool(gone) and bool(name_candidates(name) & gone)


def cud_key(res: dict) -> tuple[str, str]:
    """FHIR ClinicalUseDefinition → (藥物頁 slug, 適應症名稱)；subject 是 MedicationKnowledge/<slug>。"""
    ref = ((res.get("subject") or [{}])[0].get("reference") or "").split("/", 1)[-1]
    name = (((res.get("indication") or {}).get("diseaseSymptomProcedure") or {}).get("concept") or {}).get("text") or ""
    return ref, name


def published_withdrawn(docs: Path, table: dict[str, set[str]] | None = None) -> list[str]:
    """撤回的預測還出現在搜尋索引、FHIR、證據監測清單的位置（gate 用）。"""
    table = load() if table is None else table
    if not table:
        return []
    out = []
    si = docs / "data" / "search-index.json"
    if si.exists():
        for d in json.loads(si.read_text(encoding="utf-8")).get("drugs", []):
            out += [f"search-index：{d.get('slug')}／{i.get('name')}" for i in d.get("indications") or []
                    if is_withdrawn(table, d.get("slug"), i.get("name"))]
    cud = docs / "fhir" / "ClinicalUseDefinition"
    if cud.is_dir():
        for f in sorted(cud.glob("*.json")):
            if is_withdrawn(table, *cud_key(json.loads(f.read_text(encoding="utf-8")))):
                out.append(f"FHIR：{f.name}")
    dl = docs.parent / "scripts" / "drug_list.json"
    if dl.exists():
        data = json.loads(dl.read_text(encoding="utf-8"))
        for d in data.get("drugs", data) if isinstance(data, dict) else data:
            if isinstance(d, dict):
                slug = (d.get("file") or d.get("slug") or "").removesuffix(".md")
                out += [f"證據監測：{slug}／{n}" for n in d.get("indications") or d.get("predicted_indications") or []
                        if isinstance(n, str) and is_withdrawn(table, slug, n)]
    return out
