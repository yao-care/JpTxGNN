#!/usr/bin/env python3
"""在 FHIR metadata（CapabilityStatement）寫入本次建置實際輸出的資源數。

用法：python3 scripts/stamp_fhir_counts.py <fhir 目錄>
  - pages.yml 在 Jekyll 建置後對 ./_site/fhir 跑：數的是這次真的會部署出去的檔案。
  - 也可以對 docs/fhir 跑，讓 repo 裡的 metadata 跟檔案一致。

寫入的內容（yao.care 官網讀這個 extension 加總 30 站，2026-11-13 雙方約定的規格）：
  "date": 計數當天（Asia/Taipei）
  "extension": [{"url": "https://yao.care/fhir/StructureDefinition/txgnn-resource-counts",
                 "extension": [MedicationKnowledge 檔數, ClinicalUseDefinition 檔數, countedAt]}]
  - 只數 MedicationKnowledge/*.json、ClinicalUseDefinition/*.json；不含 Bundle 與 metadata 本身。
    撤回的預測本來就不輸出，不會算進去。
  - 已有的其他 extension 保留，同 url 只留一筆。有 metadata.json 的站兩份都寫。
  - description 裡的資源數句子統一改寫成 "Contains {MK} drugs and {CUD} predicted indications."，
    其他文字不動。
  - Bundle/all-predictions.json 不存在時（只有建置輸出目錄 _site/fhir 才做，加 --bundle），
    用同一批 MedicationKnowledge＋ClinicalUseDefinition 產生 collection Bundle；已存在就不動
    （有些站由自己的產生器維護這個檔）。

metadata 的路徑、檔名、其他欄位都不改。任何錯誤只印警告、exit 0，不擋部署。
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

EXT_URL = "https://yao.care/fhir/StructureDefinition/txgnn-resource-counts"
TYPES = ("MedicationKnowledge", "ClinicalUseDefinition")
TAIPEI = timezone(timedelta(hours=8))
COUNT_SENTENCES = [
    re.compile(r"\s*Contains [^.。]*[.。]?"),
    re.compile(r"\s*\d+\s*医薬品、\s*\d+\s*予測適応症を含む。?"),
]


def count_files(fhir: Path) -> dict[str, int]:
    return {t: len(list((fhir / t).glob("*.json"))) if (fhir / t).is_dir() else 0 for t in TYPES}


def new_description(desc: str, mk: int, cud: int) -> str:
    base = desc
    for pat in COUNT_SENTENCES:
        base = pat.sub("", base)
    base = base.strip()
    if base and not base.endswith((".", "。", "!", "?")):
        base += "."
    sentence = f"Contains {mk} drugs and {cud} predicted indications."
    if not base:
        return sentence
    return f"{base}{sentence}" if base.endswith("。") else f"{base} {sentence}"


def stamp_metadata(fhir: Path, counts: dict[str, int], today: str) -> bool:
    changed = _stamp_one(fhir / "metadata", counts, today)
    if (fhir / "metadata.json").exists():  # 有些站另有一份，內容要跟 metadata 一樣（各站 gate 會比）
        changed = _stamp_one(fhir / "metadata.json", counts, today) or changed
    return changed


def _stamp_one(mpath: Path, counts: dict[str, int], today: str) -> bool:
    if not mpath.exists():
        print(f"⚠ {mpath} 不存在，跳過")
        return False
    raw = mpath.read_text(encoding="utf-8")
    meta = json.loads(raw)
    if meta.get("resourceType") != "CapabilityStatement":
        print(f"⚠ {mpath} 不是 CapabilityStatement，跳過")
        return False
    ext = {
        "url": EXT_URL,
        "extension": [
            {"url": "MedicationKnowledge", "valueInteger": counts["MedicationKnowledge"]},
            {"url": "ClinicalUseDefinition", "valueInteger": counts["ClinicalUseDefinition"]},
            {"url": "countedAt", "valueDate": today},
        ],
    }
    others = [e for e in (meta.get("extension") or []) if e.get("url") != EXT_URL]
    meta["extension"] = others + [ext]
    meta["date"] = today
    if isinstance(meta.get("description"), str):
        meta["description"] = new_description(
            meta["description"], counts["MedicationKnowledge"], counts["ClinicalUseDefinition"])
    out = json.dumps(meta, ensure_ascii=False, indent=2) + "\n"
    if out != raw:
        mpath.write_text(out, encoding="utf-8")
        return True
    return False


def make_bundle(fhir: Path, base_url: str) -> int | None:
    bpath = fhir / "Bundle" / "all-predictions.json"
    if bpath.exists():
        return None
    entries = []
    for t in TYPES:
        d = fhir / t
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.json")):
            res = json.loads(f.read_text(encoding="utf-8"))
            rid = res.get("id") or f.stem
            entries.append({"fullUrl": f"{base_url}/fhir/{t}/{rid}", "resource": res})
    bundle = {
        "resourceType": "Bundle",
        "id": "all-predictions",
        "type": "collection",
        "timestamp": datetime.now(TAIPEI).isoformat(timespec="seconds"),
        "total": len(entries),
        "link": [{"relation": "self", "url": f"{base_url}/fhir/Bundle/all-predictions.json"}],
        "entry": entries,
    }
    bpath.parent.mkdir(parents=True, exist_ok=True)
    bpath.write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    return len(entries)


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    unknown = flags - {"--bundle"}
    if len(args) != 1 or unknown:
        print("用法：stamp_fhir_counts.py <fhir 目錄> [--bundle]")
        return 2
    fhir = Path(args[0])
    try:
        counts = count_files(fhir)
        today = datetime.now(TAIPEI).strftime("%Y-%m-%d")
        changed = stamp_metadata(fhir, counts, today)
        print(f"FHIR 資源數：MedicationKnowledge {counts['MedicationKnowledge']}、"
              f"ClinicalUseDefinition {counts['ClinicalUseDefinition']}、countedAt {today}"
              f"（metadata {'已更新' if changed else '不變'}）")
        if "--bundle" in flags:
            meta = json.loads((fhir / "metadata").read_text(encoding="utf-8"))
            base = re.sub(r"/fhir/metadata/?$", "", meta.get("url", "")).rstrip("/")
            if not base.startswith("https://"):
                print(f"⚠ metadata url 看不出網域（{meta.get('url')!r}），不產生 Bundle")
            else:
                n = make_bundle(fhir, base)
                print("Bundle/all-predictions.json 已存在，不動" if n is None
                      else f"產生 Bundle/all-predictions.json：{n} 筆")
    except Exception as e:  # 不擋部署
        print(f"⚠ stamp_fhir_counts 失敗：{e!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
