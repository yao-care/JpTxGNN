"""產生各站 docs/_data/drug_stats.json（首頁 D3 圖表資料，2026-10-17，T-307）。

只收可收錄的藥物頁（排除 ID 轉址頁、noindex、nav_exclude）。TwTxGNN 有自己的 scripts/generate_drug_stats.py，不在此處理。
欄位與原檔相同：total_drugs、level_counts、all_drugs[{name, slug, level, indication_count}]；slug＝檔名（D3 以 drugUrls 對應實際網址）。
用法：python3 .claude/gen_drug_stats.py [站 ...]
"""
import json, re, subprocess, sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def fm_get(head, key):
    m = re.search(rf"^{key}:\s*(.+?)\s*$", head, re.M)
    return m.group(1).strip('"').strip("'") if m else None


def main(argv):
    sites = argv or [p.name for p in sorted(BASE.glob("*TxGNN")) if p.name != "TwTxGNN"]
    for s in sites:
        proj = BASE / s
        # 2026-10-27：站上有 scripts/generate_drug_stats.py（drugs.md 建置守門用的同一套規則）就交給它，免得兩套規則不一致讓建置失敗
        if (proj / "scripts/generate_drug_stats.py").exists():
            r = subprocess.run([sys.executable, "scripts/generate_drug_stats.py"], cwd=proj, capture_output=True, text=True)
            print(f"{s}: {r.stdout.strip().splitlines()[0] if r.stdout.strip() else ''}{'（' + r.stdout.strip().splitlines()[-1] + '）' if r.returncode else ''}")
            continue
        out = proj / "docs/_data/drug_stats.json"
        drugs = []
        for f in sorted((proj / "docs/_drugs").glob("*.md")):
            t = f.read_text(encoding="utf-8", errors="replace")
            head = t[:2000]
            if 'http-equiv="refresh"' in t or re.search(r"^(noindex|nav_exclude):\s*true", head, re.M):
                continue
            lv = fm_get(head, "evidence_level") or "L5"
            ic = fm_get(head, "indication_count") or "0"
            drugs.append({"name": fm_get(head, "title") or f.stem, "slug": f.stem, "level": lv,
                          "indication_count": int(ic) if ic.isdigit() else 0})
        counts = {f"L{n}": sum(d["level"] == f"L{n}" for d in drugs) for n in range(1, 6)}
        data = {"generated": date.today().isoformat(), "total_drugs": len(drugs), "level_counts": counts, "all_drugs": drugs}
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{s}: {len(drugs)} {counts}")


if __name__ == "__main__":
    main(sys.argv[1:])
