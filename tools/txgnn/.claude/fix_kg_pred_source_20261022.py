"""藥物頁本文把知識圖譜（KG）寫成預測來源的句子（2026-10-22，pm：不用 LLM、只改預測來源用語）。

只改明確的句型（KG 分數／KG 預測／依知識圖譜預測）→ 該站語言的「TxGNN 模型（深度學習）」；其餘一字不動。
已在重生 2,117／已知用途 479／無預測 1,200 名單內的頁跳過（跟著那條線重寫）。
「分數反映知識圖譜上的接近程度」這類解釋句不改，列為待審。頁面與 notes 同步改（--apply 才寫檔）。
輸出 .claude/audit_20261016/kg_pred_source/：changes.diff、lines.tsv（每行：site, page, line, status, text）
用法（母目錄）：python3 .claude/fix_kg_pred_source_20261022.py [--apply]
"""
import csv
import difflib
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / ".claude/audit_20261016/kg_pred_source"
LANG = {"ARTxGNN": "es", "COTxGNN": "es", "ESTxGNN": "es", "BrTxGNN": "pt", "CHTxGNN": "de", "DETxGNN": "de", "DkTxGNN": "da",
        "FITxGNN": "fi", "FRTxGNN": "fr", "HkTxGNN": "zh", "TwTxGNN": "zh", "ITTxGNN": "it", "JpTxGNN": "ja", "KrTxGNN": "ko",
        "MyTxGNN": "ms", "NlTxGNN": "nl", "NOTxGNN": "no", "SATxGNN": "ar", "SETxGNN": "sv", "ThTxGNN": "th"}
# 句型 → 替換（只換「預測來源」名詞片語）
RULES = {
    "en": [(r"(?:model |computational )?prediction from (?:the |a )?knowledge graph", "prediction from the TxGNN model (deep learning)"),
           (r"knowledge[- ]graph (artefact|artifact)", r"TxGNN model (deep learning) \1"),
           (r"predicted based on (?:the )?TxGNN knowledge graph(?: analysis)?", "predicted by the TxGNN model (deep learning)"),
           (r"knowledge[- ]graph[- ]based prediction", "TxGNN model (deep learning) prediction"),
           (r"knowledge[- ]graph (score|prediction)", r"TxGNN model (deep learning) \1"),
           (r"(?:a |the )?knowledge-graph (score|prediction)", r"a TxGNN model (deep learning) \1")],
    "es": [(r"predicci[oó]n sobre el grafo de conocimiento", "predicción del modelo TxGNN (aprendizaje profundo)"),
           (r"se basa (solo|únicamente|unicamente) en el grafo de conocimiento", r"se basa \1 en el modelo TxGNN (aprendizaje profundo)"),
           (r"artefactos? del grafo de conocimiento", lambda m: m.group(0).split(" del ")[0] + " del modelo TxGNN (aprendizaje profundo)"),
           (r"predicci[oó]n (?:basada en el|del) grafo de conocimiento", "predicción del modelo TxGNN (aprendizaje profundo)"),
           (r"puntuaci[oó]n (muy alta |alta )?del grafo de conocimiento", r"puntuación \1del modelo TxGNN (aprendizaje profundo)")],
    "pt": [(r"previs[ãa]o baseada (?:em|no) grafo de conhecimento", "previsão do modelo TxGNN (aprendizado profundo)"),
           (r"(?<!contraindicações )(?<!contraindicacoes )previst([ao]s?) pelo grafo de conhecimento", r"previst\1 pelo modelo TxGNN (aprendizado profundo)")],
    "fr": [(r"pr[ée]diction (?:par|fond[ée]e sur un) graphe de connaissances", "prédiction du modèle TxGNN (apprentissage profond)"),
           (r"pr[ée]diction (?:fond[ée]e sur le|du) graphe de connaissances", "prédiction du modèle TxGNN (apprentissage profond)")],
    "it": [(r"previsione (?:basata su|del) grafo di conoscenza", "previsione del modello TxGNN (apprendimento profondo)")],
    "de": [(r"Vorhersage (?:aus dem|auf Basis eines) Wissensgraphen", "Vorhersage des TxGNN-Modells (Deep Learning)"),
           (r"Score im Wissensgraphen", "Score des TxGNN-Modells (Deep Learning)"),
           (r"Artefakt des Wissensgraphen", "Artefakt des TxGNN-Modells (Deep Learning)"),
           (r"Wissensgraph-Vorhersage(n?)", r"Vorhersage\1 des TxGNN-Modells (Deep Learning)"),
           (r"Vorhersagewert des Wissensgraph(?:en|s)?", "Vorhersagewert des TxGNN-Modells (Deep Learning)")],
    "ja": [(r"知識グラフ上の関係性から導かれた予測", "TxGNN モデル（深層学習）による予測"),
           (r"知識グラフ上の関連に基づく計算上のもの", "TxGNN モデル（深層学習）による計算上のもの")],
    "nl": [(r"voorspelling op basis van een kennisgraaf", "voorspelling van het TxGNN-model (deep learning)")],
    "no": [(r"prediksjon fra kunnskapsgrafen?", "prediksjon fra TxGNN-modellen (dyp læring)")],
    "sv": [(r"kunskapsgrafsprediktion(en)?", r"prediktion\1 från TxGNN-modellen (djupinlärning)")],
    "da": [(r"videngraf-forudsigelse(n)?", r"forudsigelse\1 fra TxGNN-modellen (dyb læring)")],
    "zh": [(r"分數僅來自知識圖譜", "分數僅來自 TxGNN 模型（深度學習）"),
           (r"預測可能來自知識圖譜", "預測來自 TxGNN 模型（深度學習）")],
    "ms": [(r"ramalan graf pengetahuan", "ramalan model TxGNN (pembelajaran mendalam)")],
    "ar": [(r"التنبؤ المبني على الرسم البياني المعرفي", "التنبؤ المبني على نموذج TxGNN (التعلم العميق)")],
}
KG = (r"knowledge[- ]graph|wissensgraph|graphe de connaissances|grafo de conoc|grafo de conhec|grafo di conoscenza|kennisgraaf|"
      r"kunnskapsgraf|kunskapsgraf|videngraf|tietograaf|知識圖譜|知識グラフ|지식 ?그래프|graf pengetahuan|الرسم البياني المعرفي")
PRED = (r"score|scor|punt|pontua|punteggio|pistem|poäng|poeng|分數|分数|スコア|점수|skor|درجة|คะแนน|predict|prédi|previs|predic|"
        r"vorhersag|voorspel|prediks|prediktion|forudsig|ennust|預測|予測|예측|ramal|التنبؤ|คาดการณ์")
HIT = re.compile(r"(" + KG + r")[^.。\n|]{0,25}(" + PRED + r")|(" + PRED + r")[^.。\n|]{0,25}(" + KG + r")", re.I)
OK = re.compile(r"exclud|known use|already recorded|not (a )?predict|trained on|ausgeschlossen|bekannt|exclu|connu|conocid|conhecid|"
                r"esclus|排除|已知|既知|除外|제외|기존|dikecualikan|diketahui|مستبعد|معروف|ตัดออก|ทราบ", re.I)


def listed():
    s = set()
    for f, col in ((".claude/audit_20261016/track4/main_excluded.tsv", "page"), (".claude/audit_20261016/track4/all_known.tsv", "page"),
                   (".claude/audit_20261016/no_prediction_099.tsv", "page")):
        with open(BASE / f, encoding="utf-8") as fh:
            s |= {(r["site"], r[col]) for r in csv.DictReader(fh, delimiter="\t")}
    return s


def main(argv):
    apply_ = "--apply" in argv
    OUT.mkdir(parents=True, exist_ok=True)
    skip = listed()
    rows, diffs = [], []
    for f in sorted(BASE.glob("*TxGNN/docs/_drugs/*.md")):
        s, page = f.parts[-4], f.stem
        raw = f.read_bytes().decode("utf-8", errors="replace")
        if 'http-equiv="refresh"' in raw[:3000]:
            continue
        crlf = "\r\n" in raw[:500]
        t = raw.replace("\r\n", "\n")
        lines = t.split("\n")
        new = list(lines)
        for i, l in enumerate(lines):
            if l.startswith(("description:", "title:")) or not HIT.search(l) or OK.search(l):
                continue
            if (s, page) in skip or (s, page.replace("-", "_")) in skip:
                rows.append((s, page, i + 1, "skipped_in_regen_list", l.strip()[:200])); continue
            l2 = l
            for a, b in RULES.get(LANG.get(s, "en"), []):
                l2 = re.sub(a, b, l2, flags=re.I)
            if l2 != l:
                new[i] = l2
                rows.append((s, page, i + 1, "auto_fixed", l2.strip()[:200]))
            else:
                rows.append((s, page, i + 1, "review_not_changed", l.strip()[:200]))
        if new != lines:
            t2 = "\n".join(new)
            diffs += difflib.unified_diff(t.splitlines(True), t2.splitlines(True), f"a/{s}/docs/_drugs/{f.name}", f"b/{s}/docs/_drugs/{f.name}", n=0)
            if apply_:
                f.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
                nb = BASE / s / "data/notes" / page / "drug_pharmacist_notes.md"
                if nb.exists():
                    nt = nb.read_text(encoding="utf-8")
                    for a_, b_ in zip(lines, new):
                        if a_ != b_ and nt.count(a_) == 1:
                            nt = nt.replace(a_, b_)
                    nb.write_text(nt, encoding="utf-8")
    (OUT / "changes.diff").write_text("".join(diffs), encoding="utf-8")
    with open(OUT / "lines.tsv", "w", encoding="utf-8") as fh:
        fh.write("site\tpage\tline\tstatus\ttext\n")
        for r in rows:
            fh.write("\t".join(map(str, r)) + "\n")
    import collections
    c = collections.Counter(r[3] for r in rows)
    print(dict(c), "頁數", {k: len({(r[0], r[1]) for r in rows if r[3] == k}) for k in c})


if __name__ == "__main__":
    main(sys.argv[1:])
