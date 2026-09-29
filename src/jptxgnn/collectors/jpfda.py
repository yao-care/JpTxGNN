"""本國藥證收集器（NEW_COUNTRY_SOP Phase 5：collectors/{cc}fda.py）。

資料全部走 Phase 1 的標準產物，不寫死任何國家的檔名或欄位：
- 本國藥證：data/loader.py 的 load_fda_drugs()（本站自己的 {cc}_fda_drugs.json）
- 欄位對照：config/fields.yaml 的 field_mapping / withdrawn_statuses
- 藥名 → DrugBank ID → 許可證：data/processed/drug_mapping.csv（Phase 1 對照結果）
  與 data/external/drugbank_vocab.csv（英文藥名 → DrugBank ID）

藥名對到 DrugBank ID 再回查許可證，所以本國藥證是日文、韓文、泰文也對得上。
回傳格式與 TwTxGNN 的 TFDACollector 相同（found / records / total_matches / package_insert），
drug_bundle.py 與 drug_evidence_pack.py 不需要改。
"""

import csv
import re
import unicodedata
from pathlib import Path

from .base import BaseCollector, CollectorResult

PROJECT_ROOT = Path(__file__).resolve().parents[3]

LICENSE_COLS = ("license_id", "承認番号", "許可證字號", "reg_no")
INGREDIENT_COLS = ("normalized_ingredient", "標準化成分")
SUCCESS_COLS = ("mapping_success", "映射成功")


def _norm(text) -> str:
    text = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _key(text) -> str:
    """原文（保留非拉丁字母）去空白轉小寫，給日文／韓文等成分名比對用。"""
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


# fields.yaml 缺檔或欄名與 loader 輸出不符時（Au/Ca/Dk/Hk/Uk/Za 的 loader 會正規化欄名），改用 loader 實際輸出的欄位
COLUMN_ALIASES = {
    "ingredients": ("ingredients", "Active_Ingredients", "Active_Substances", "active_substance", "short_composition1", "INGREDIENT"),
    "brand_name_local": ("brand_name", "Product_Name", "name", "productName"),
    "brand_name_en": ("brand_name", "Product_Name", "inn_name", "name"),
    "license_id": ("license_id", "ARTG_ID", "License_Number", "PL_Number", "regno", "MPR_ID", "id"),
    "indication": ("indication", "therapeutic_indication"),
    "dosage_form": ("dosage_form", "Dosage_Form", "pack_size_label"),
    "manufacturer": ("manufacturer", "Manufacturer", "holder_name", "manufacturer_name"),
    "approval_date": ("approval_date",),
    "status": ("status",),
}


def _load_config() -> dict:
    from ..data import loader

    fn = getattr(loader, "load_config", None) or getattr(loader, "load_field_config", None)
    try:
        return (fn() if fn else {}) or {}
    except (FileNotFoundError, OSError):  # Dk/Za 沒有 config/fields.yaml
        return {}


class LocalFDACollector(BaseCollector):
    """本國藥證查詢（讀 Phase 1 標準資料）。"""

    source_name = "local_fda"

    def __init__(self):
        self._ready = False

    def _prepare(self):
        if self._ready:
            return
        from ..data.loader import load_fda_drugs

        cfg = _load_config()
        self.fm = dict(cfg.get("field_mapping") or {})
        self.withdrawn = {str(s).strip().lower() for s in (cfg.get("withdrawn_statuses") or []) if str(s).strip()}

        df = load_fda_drugs()
        cols = set(df.columns)
        for k, aliases in COLUMN_ALIASES.items():
            if self.fm.get(k) not in cols:
                self.fm[k] = next((a for a in aliases if a in cols), self.fm.get(k))
        self.records = df.to_dict("records")
        ing_field = self.fm.get("ingredients")
        for rec in self.records:
            rec["_ing_norm"] = " " + _norm(rec.get(ing_field, "")) + " " if ing_field else " "

        # drug_mapping.csv：成分名 → DrugBank ID、DrugBank ID → 許可證
        self.ing_to_db, self.db_to_lic = {}, {}
        mp = PROJECT_ROOT / "data" / "processed" / "drug_mapping.csv"
        with open(mp, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            cols = reader.fieldnames or []
            lic_col = next((c for c in LICENSE_COLS if c in cols), None)
            ing_col = next((c for c in INGREDIENT_COLS if c in cols), None)
            ok_col = next((c for c in SUCCESS_COLS if c in cols), None)
            for row in reader:
                db = str(row.get("drugbank_id", "") or "").strip().upper()
                if not db or (ok_col and str(row.get(ok_col)).strip().lower() not in ("true", "1", "yes")):
                    continue
                if ing_col:
                    for k in {_norm(row[ing_col]), _key(row[ing_col])}:
                        if k:
                            self.ing_to_db.setdefault(k, set()).add(db)
                if lic_col and row.get(lic_col):
                    self.db_to_lic.setdefault(db, set()).add(str(row[lic_col]).strip())

        # 以哪一欄對 drug_mapping 的許可證號：先用 fields.yaml 的 license_id；若重疊太少
        # （例：Us 的 mapping 存 ProductNDC、fields.yaml 寫 ApplNo），改用重疊最多的欄位
        sample = {lic for lics in self.db_to_lic.values() for lic in lics}
        def overlap(col):
            return sum(1 for r in self.records if str(r.get(col, "") or "").strip() in sample)
        cols = [self.fm.get("license_id")] + [c for c in (self.records[0].keys() if self.records else []) if c != self.fm.get("license_id")]
        best = max((c for c in cols if c), key=overlap, default=None)
        self.join_col = self.fm.get("license_id") if best is None or overlap(self.fm.get("license_id") or "") >= 0.5 * overlap(best) else best
        self.by_license = {}
        for rec in self.records:
            lic = str(rec.get(self.join_col, "") or "").strip()
            if lic:
                self.by_license.setdefault(lic, []).append(rec)

        # drugbank_vocab.csv：英文藥名 → DrugBank ID
        self.name_to_db = {}
        vocab = PROJECT_ROOT / "data" / "external" / "drugbank_vocab.csv"
        if vocab.exists():
            with open(vocab, encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    self.name_to_db.setdefault(_norm(row.get("drug_name")), set()).add(str(row.get("drugbank_id", "")).upper())
        self._ready = True

    def _drugbank_ids(self, drug: str) -> set:
        ids = set()
        m = re.fullmatch(r"\s*(DB\d{5})\s*", str(drug or ""), re.I)
        if m:
            ids.add(m.group(1).upper())
        for k in (_norm(drug), _key(drug)):
            ids |= self.ing_to_db.get(k, set()) | self.name_to_db.get(k, set())
        return ids

    def _text_match(self, drug: str) -> list:
        core = _norm(drug)
        if len(core) < 4:
            return []
        if " " not in core and len(core) >= 6:
            pat = re.compile(rf" {re.escape(core)}[a-z]{{0,3}} ")  # metformin → metformina / metformine
            return [r for r in self.records if pat.search(r["_ing_norm"])]
        return [r for r in self.records if f" {core} " in r["_ing_norm"]]

    def _is_withdrawn(self, rec: dict) -> bool:
        sf = self.fm.get("status")
        if not sf or not self.withdrawn:
            return False
        val = str(rec.get(sf, "") or "").strip().lower()
        return any(w and w in val for w in self.withdrawn)

    def search(self, drug: str, disease: str | None = None, drugbank_id: str | None = None) -> CollectorResult:
        query = {"drug": drug, "disease": disease}
        try:
            self._prepare()
            ids = self._drugbank_ids(drug)
            if drugbank_id:
                ids.add(str(drugbank_id).upper())
            recs = []
            for db in ids:
                for lic in self.db_to_lic.get(db, ()):
                    recs.extend(self.by_license.get(lic, []))
            if not recs:
                # Phase 1 對照沒對上的成分（例：重音字未正規化）→ 退回比對本國藥證的成分欄
                recs = self._text_match(drug)
            active = [r for r in recs if not self._is_withdrawn(r)]
            return self._make_result(query=query, data=self._format(active, ids), success=True)
        except Exception as e:  # noqa: BLE001 — 與其他 collector 一致：失敗時回 not found 並帶錯誤
            return self._make_result(query=query, data={"found": False, "records": []}, success=False, error_message=str(e))

    def _format(self, records: list, ids: set) -> dict:
        if not records:
            return {"found": False, "records": [], "drugbank_ids": sorted(ids)}
        # 單一成分產品排前面（報告只取前幾筆許可證），複方排後面
        ing_f = self.fm.get("ingredients")
        records = sorted(records, key=lambda r: len(re.split(r"[,;+/&]|&&| and | y | e | und | et ", str(r.get(ing_f, "") or ""))) if ing_f else 0)
        g = lambda r, k: str(r.get(self.fm.get(k) or "", "") or "").strip() if self.fm.get(k) else ""  # noqa: E731
        out = [
            {
                "license_id": g(r, "license_id"),
                "brand_name_zh": g(r, "brand_name_local"),
                "brand_name_en": g(r, "brand_name_en"),
                "ingredients": g(r, "ingredients"),
                "indication": g(r, "indication"),
                "dosage_form": g(r, "dosage_form"),
                "manufacturer": g(r, "manufacturer"),
                "license_holder": g(r, "manufacturer"),
                "approval_date": g(r, "approval_date"),
                "expiry_date": "",
                "status": g(r, "status"),
            }
            for r in records[:20]
        ]
        return {
            "found": True,
            "records": out,
            "total_matches": len(records),
            "drugbank_ids": sorted(ids),
            "package_insert": {"warnings": [], "contraindications": [], "dosage": "", "special_populations": []},
        }
