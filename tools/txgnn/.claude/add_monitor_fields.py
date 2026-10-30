"""替藥物名稱頁的 front matter 寫入新文獻監測用欄位（2026-10-16，check-new-evidence 修正 a）。

  monitor_inn: "<證據包 drug.inn>"
  predicted_indications: ["<英文疾病名>", ...]   # 證據包 predicted_indications 前 10 名

只寫 front matter，不渲染、不進 JSON-LD。證據包沒有新預測的頁不寫（監測會跳過）。
sync_notes_to_docs.py 重生頁面時會用同一個函式（monitor_fields）寫回，兩邊口徑一致。

用法：python3 .claude/add_monitor_fields.py [站 ...]
"""
import json, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
KEYS = ("monitor_inn", "predicted_indications")


def load_bundle(proj: Path, stem: str):
    for c in (stem, stem.replace("-", "_"), stem.lower(), stem.lower().replace("-", "_")):
        b = proj / "data/bundles" / c / "drug_bundle.json"
        if b.exists():
            try:
                return json.load(open(b, encoding="utf-8"))
            except Exception:
                return None
    return None


_KF = None


def _kf():
    global _KF
    if _KF is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("known_use_filter", BASE / ".claude/known_use_filter.py")
        _KF = importlib.util.module_from_spec(spec); spec.loader.exec_module(_KF)
    return _KF


def monitor_fields(bundle, proj: Path = None) -> list[str]:
    if not bundle:
        return []
    d = bundle.get("drug") or {}
    inn = (d.get("inn") or d.get("name") or "").strip()  # MyTxGNN 等站的證據包用 name
    if proj is not None:  # N-01／N-04＋0.99 門檻（2026-10-22）：與 reviewer、sync 共用 kept_predictions
        names = _kf().kept_predictions(proj, bundle)
    else:
        names = [p.get("disease_name", "").strip() for p in (d.get("predicted_indications") or []) if p.get("disease_name")][:10]
    if not names or not inn:
        return []
    return [f"monitor_inn: {json.dumps(inn, ensure_ascii=False)}",
            f"predicted_indications: {json.dumps(names, ensure_ascii=False)}"]


def apply(path: Path, lines: list[str]) -> bool:
    b = path.read_bytes()
    nl = b"\r\n" if b"\r\n" in b[:300] else b"\n"
    m = re.match(rb"(?:\xef\xbb\xbf)?---\r?\n(.*?)\r?\n---\r?\n", b, re.S)
    if not m:
        return False
    fm = m.group(1).decode("utf-8").splitlines()
    if [l for l in fm if l.split(":", 1)[0].strip() in KEYS] == lines:
        return False  # 內容相同就不搬動位置
    fm = [l for l in fm if not l.split(":", 1)[0].strip() in KEYS]
    fm += lines
    new = b[:m.start(1)] + nl.join(l.encode("utf-8") for l in fm) + b[m.end(1):]
    if new != b:
        path.write_bytes(new)
        return True
    return False


def main(argv):
    sites = argv or [p.name for p in sorted(BASE.glob("*TxGNN"))]
    for s in sites:
        proj = BASE / s
        n = w = 0
        for f in sorted((proj / "docs/_drugs").glob("*.md")):
            if re.fullmatch(r"db\d{5}", f.stem.lower()):
                continue
            lines = monitor_fields(load_bundle(proj, f.stem), proj)
            n += bool(lines)
            w += apply(f, lines)
        print(f"{s}: 有預測 {n} 頁，寫入／更新 {w} 頁")


if __name__ == "__main__":
    main(sys.argv[1:])
