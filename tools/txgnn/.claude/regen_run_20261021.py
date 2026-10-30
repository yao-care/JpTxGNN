"""重生主預測被排除的頁（2026-10-21，r5 基準；用戶核准、pm 驗過 precheck 後執行）。

每個藥：該站 batch_generate_reports.py --drugs X --no-skip（reviewer 已接 r5 過濾，部分紀錄張數寫 ≥N）
→ 新報告自動驗收，不過就還原舊 notes（.claude/cache/notes_backup_20261021/），失敗稿存 .claude/cache/regen_fail/
→ 通過的藥最後用 SYNC_ONLY 只重寫這些頁（其他頁在 docs 上的直接修正不會被 notes 覆蓋）。
驗收：
  1. 已排除的適應症（證據包原始預測 − r5 保留）英文名不得出現
  2. 不得把 KG 寫成預測
  3. 報告裡的 PMID／NCT 必須都在證據包裡
  4. 事實是 Marketed 時，概覽表市場狀態列不得寫成註銷／未上市
  5. 表格不得出現 None
用法（母目錄）：python3 .claude/regen_run_20261021.py --list site:drug,... | --tsv 檔 [--part i/n] [--no-sync]
結果逐行附加到 .claude/audit_20261016/regen_results.tsv
"""
import os as _os, sys as _sys
if __name__ == "__main__" and _os.environ.get("ALLOW_AI_REGEN") != "1" and "--selftest" not in _sys.argv:
    _sys.exit("已停用（2026-10-28）：藥物頁事實改由 .claude/factlayer_20261028.py 程式產生，不再用 AI 整頁重生。"
              "確定要用 AI 重產時，先經 pm 同意並試跑 20 頁，再以 ALLOW_AI_REGEN=1 執行。")
import csv
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BK = BASE / ".claude/cache/notes_backup_20261021"
FAIL = BASE / ".claude/cache/regen_fail"
RES = BASE / ".claude/audit_20261016/regen_results.tsv"
_s = importlib.util.spec_from_file_location("kf", BASE / ".claude/known_use_filter.py")
kf = importlib.util.module_from_spec(_s); _s.loader.exec_module(kf)
_s = importlib.util.spec_from_file_location("mv2", BASE / ".claude/rewrite_market_v2_20261021.py")
mv2 = importlib.util.module_from_spec(_s); _s.loader.exec_module(mv2)
KG_AS_PRED = re.compile(r"knowledge graph (model )?predict|KG[- ]prediction|\|\s*KG\s*\|\s*$|predicted by the knowledge graph", re.I | re.M)


GENERIC_WORDS = {"chronic", "primary", "acute", "cancer", "carcinoma", "disease", "disorder", "syndrome", "type", "familial",
                 "hereditary", "congenital", "infection", "deficiency", "susceptibility", "neoplasm", "tumor", "tumour", "malignant",
                 "benign", "early", "onset", "adult", "childhood", "juvenile", "severe", "related", "associated", "induced",
                 "secondary", "idiopathic", "infectious", "the", "and", "due", "autosomal", "dominant", "recessive", "with", "without", "unspecified", "other"}
# 同義詞、縮寫、子型（病名 → 文獻標題裡出現就算直接研究本病）
SYNONYMS = {
    "ankylosing spondylitis": [r"\bAS\b", r"axial spondyloarthritis", r"\baxSpA\b", r"spondyloarthritis"],
    "chronic lymphocytic leukemia": [r"\bCLL\b", r"small lymphocytic lymphoma"],
    "trigeminal autonomic cephalalgia": [r"cluster headache", r"\bSUNCT\b", r"\bSUNA\b", r"paroxysmal hemicrania", r"hemicrania continua"],
    "gastroduodenitis": [r"gastroduodenal ulcer", r"duodenal ulcer", r"gastric ulcer", r"peptic ulcer", r"gastritis", r"duodenitis"],
    "multiple sclerosis": [r"\bMS\b", r"\bRRMS\b", r"\bSPMS\b", r"\bPPMS\b"],
    "non-small cell lung": [r"\bNSCLC\b"],
    "toxemia of pregnancy": [r"pre-?eclampsia", r"\beclampsia"],  # 2026-10-29：子癇前症＝妊娠毒血症（用戶核准，Tw 硫酸鎂人工重審 L1）
    r"(?<!non-)(?<!non )small cell lung": [r"(?<!non-)(?<!non )\bSCLC\b"],
}


MODIFIERS = {"ovarian", "renal", "hepatic", "pulmonary", "cutaneous", "skin", "pediatric", "paediatric", "childhood", "recurrent",
             "refractory", "metastatic", "advanced", "localized", "localised", "bilateral", "adult", "elderly", "uterine", "gastric",
             "intestinal", "ocular", "oral", "nasal", "spinal", "cerebral", "primary", "secondary"}
# 同層級區分詞：病名裡有就必須在標題裡出現（B 肝 vs C 肝、第 1 型 vs 第 2 型、NSCLC vs SCLC）
DISCRIM = re.compile(r"(?<![a-z0-9])([a-z]|\d{1,2}|non|small|large|type)(?![a-z0-9])", re.I)


def direct_evidence(disease, titles):
    """標題是否直接研究本病（2026-10-22 pm 第 4–6 點）：
    - 核心詞（去泛用詞）都要出現；部位／修飾詞（ovarian、metastatic…）可省略＝母病文獻可算子型（由上往下）
    - 區分詞（單一字母、數字、non/small/type）病名有就必須出現，避免 B 肝↔C 肝、1 型↔2 型、NSCLC↔SCLC 互通
    - 同義詞／縮寫表（AS、CLL、MS、NSCLC、TAC 子型…）
    - 不再用疾病類別比對（類別會讓同層級的不同病互通）"""
    low = titles.lower()
    d = disease.lower()
    words = [w for w in re.findall(r"[a-z0-9]+", d)]
    core = {w for w in words if len(w) >= 3 and w not in GENERIC_WORDS and w not in MODIFIERS}
    discrim = {m.group(1).lower() for m in DISCRIM.finditer(d)}
    def has(w):
        return re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low) is not None
    if core and all(has(w) for w in core) and all(has(w) for w in discrim):
        return True
    for k, v in SYNONYMS.items():
        if re.search(k, d) and any(re.search(s, titles) if re.search(r"[A-Z]", s) else re.search(s, titles, re.I) for s in v):
            return True
    return False


def gate(site, drug, notes):
    errs = []
    b = json.load(open(BASE / site / "data/bundles" / drug / "drug_bundle.json", encoding="utf-8"))
    d = b["drug"]
    raw = [p["disease_name"] for p in d.get("predicted_indications", [])]
    keep = kf.kept_predictions(BASE / site, b)  # ≥0.99 前 10 名＋排除已知用途（與 reviewer、sync 同口徑）
    for x in set(raw) - set(keep):
        if len(x) > 5 and re.search(r"(?<![A-Za-z])" + re.escape(x) + r"(?![A-Za-z])", notes, re.I) and \
                not any(re.search(r"(?<![A-Za-z])" + re.escape(x) + r"(?![A-Za-z])", k, re.I) for k in keep):
            errs.append(f"提到已排除的「{x}」")
    if KG_AS_PRED.search(notes):
        errs.append("把 KG 寫成預測")
    ep = next(iter(glob.glob(str(BASE / site / "data/evidence_packs" / drug / "*_drug_evidence_pack.json"))), None)
    if ep:
        e = open(ep, encoding="utf-8").read()
        for pid in set(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", notes)) | set(re.findall(r"\bNCT\d{8}\b", notes)):
            if pid not in e:
                errs.append(f"證據包沒有 {pid}")
    facts = json.loads((BASE / ".claude/cache/license_facts" / f"{site}.json").read_text()).get(drug, {})
    if facts.get("market_status") == "Marketed":
        for l in notes.split("\n"):
            c = l.split("|")
            if l.startswith("|") and len(c) >= 4 and mv2.LABEL.search(c[1]) and not mv2.COUNT_LABEL.search(c[1]) and mv2.NEG.search(c[2]):
                errs.append(f"市場狀態寫成註銷：{c[2].strip()[:40]}")
                break
    if re.search(r"\|\s*None\s*\|", notes):
        errs.append("表格出現 None")
    # 2026-10-22（pm 第 4、7 點）：每個標 L1–L4 的預測都要有直接研究該病的試驗或文獻（證據包欄位 clinical_trials／literature）
    if ep:
        epj = json.loads(e)
        by_score = {}
        for pi in epj.get("predicted_indications") or []:
            sc = (pi.get("txgnn") or {}).get("score")
            if sc is not None:
                by_score.setdefault(f"{sc * 100:.2f}", []).append(pi)
        for line in notes.split("\n"):
            if not line.startswith("|"):
                continue
            lv = re.search(r"\|\s*\**(L[1-4])\**\s*\|", line)
            sc = re.search(r"(\d{2}\.\d{2})\s*%", line)
            if not lv or not sc:
                continue
            for pi in by_score.get(sc.group(1), []):
                ev = pi.get("evidence") or {}
                titles = " ".join(str(x.get("title", "")) for k in ("clinical_trials", "ictrp_trials", "literature") for x in (ev.get(k) or []))
                if not direct_evidence(pi["disease_name"], titles):
                    errs.append(f"給 {lv.group(1)} 但證據包沒有直接研究「{pi['disease_name']}」的試驗或文獻")
        # 主預測（概覽表的等級列）
        pis = epj.get("predicted_indications") or []
        lvm = re.search(r"\|[^|\n]*(?:Evidence|證據|証據|エビデンス|근거|Evidenz|preuve|evidencia|evidência|evidenza|näytön|evidens|bewijs|الدليل|bukti|หลักฐาน)[^|\n]*\|\s*\**(L[1-5])", notes, re.I)
        if pis and lvm and lvm.group(1) != "L5":
            ev = pis[0].get("evidence") or {}
            titles = " ".join(str(x.get("title", "")) for k in ("clinical_trials", "ictrp_trials", "literature") for x in (ev.get(k) or []))
            if not direct_evidence(pis[0]["disease_name"], titles):
                errs.append(f"主預測給 {lvm.group(1)} 但證據包沒有直接研究「{pis[0]['disease_name']}」的試驗或文獻")
        # 分數必須與證據包一致（pm minor：eu bedaquiline 99.68 vs 99.70）
        valid = set(by_score)
        for m in re.finditer(r"(?<![\d.])(9\d\.\d{2})\s*%", notes):
            if m.group(1) not in valid and not any(abs(float(m.group(1)) - float(v)) < 0.005 for v in valid):
                errs.append(f"分數 {m.group(1)}% 不在證據包裡"); break
    return errs


LIMIT_RX = re.compile(r"usage limit|rate.?limit|\b429\b|overloaded|limit reached|hit your limit|limit.{0,40}resets", re.I)  # 2026-10-23 pm：撞額度要退避重試，不算失敗


def run(site, drug):
    notes = BASE / site / "data/notes" / drug / "drug_pharmacist_notes.md"
    while True:
        t0 = time.time()
        r = subprocess.run(["uv", "run", "python", "scripts/batch_generate_reports.py", "--drugs", drug, "--no-skip", "--model", "sonnet"],
                           cwd=BASE / site, capture_output=True, text=True, timeout=3600)
        new = notes.read_text(encoding="utf-8") if notes.exists() else ""
        fresh = notes.exists() and notes.stat().st_mtime > t0
        # 2026-10-23 pm：撞額度要退避重試，不算失敗、不留舊內容
        if fresh or not LIMIT_RX.search((r.stderr or "") + (r.stdout or "")):
            break
        print("額度退避 300s", file=sys.stderr, flush=True); time.sleep(300)
    errs = [] if fresh else [f"沒有產生新報告：{(r.stderr or r.stdout)[-150:]}".replace("\n", " ")]
    if fresh:
        errs = gate(site, drug, new)
        # 2026-10-23：只有「給 L1–L4 但沒有直接證據」的錯 → 照收，後處理（apply_programmatic P4）降成 L5
        if errs and all("但證據包沒有直接研究" in e for e in errs):
            with open(BASE / ".claude/audit_20261016/full_llm/p4_downgrade.tsv", "a", encoding="utf-8") as fh:
                fh.write(f"{site}\t{drug}\t{'；'.join(errs)}\n")
            errs = []
    if errs:
        if fresh:
            (FAIL / site).mkdir(parents=True, exist_ok=True)
            (FAIL / site / f"{drug}.md").write_text(new, encoding="utf-8")
        if (BK / site / drug).exists():
            shutil.rmtree(notes.parent, ignore_errors=True)
            shutil.copytree(BK / site / drug, notes.parent)
    return errs, time.time() - t0


def main(argv):
    if "--list" in argv:
        items = [tuple(x.split(":")) for x in argv[argv.index("--list") + 1].split(",")]
    else:
        targets = json.loads((BASE / ".claude/audit_20261016/regen_r5_targets.json").read_text())
        items = [(s, d) for s in sorted(targets) for d in targets[s]]
    if "--part" in argv:
        i, n = map(int, argv[argv.index("--part") + 1].split("/"))
        items = items[i::n]
    ok = {}
    for s, d in items:
        try:
            errs, sec = run(s, d)
        except Exception as e:
            errs, sec = [f"例外：{str(e)[:120]}"], 0
        with open(RES, "a", encoding="utf-8") as f:
            f.write(f"{s}\t{d}\t{'OK' if not errs else 'FAIL'}\t{'；'.join(errs)}\t{sec:.0f}\n")
        print(f"{'✓' if not errs else '✗'} {s}:{d} ({sec:.0f}s) {'；'.join(errs)[:150]}", flush=True)
        if not errs:
            ok.setdefault(s, []).append(d)
    if "--no-sync" not in argv:
        for s, ds in ok.items():
            env = dict(os.environ, SYNC_ONLY=",".join(ds))
            r = subprocess.run(["uv", "run", "python", "scripts/sync_notes_to_docs.py"], cwd=BASE / s, env=env, capture_output=True, text=True)
            print(f"sync {s}: {len(ds)} 頁 {'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[-150:]}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
