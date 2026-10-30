"""軌 5 第二版（2026-10-21）：市場狀態列＋張數列＋許可證表狀態欄，同一批程式化改寫。預設乾跑，--apply 才寫檔。

事實來源：.claude/cache/license_facts/<站>.json（dump_license_facts_20261021.py；各站修正後 reviewer._local_regulatory：
張數＝不重複許可證號，partial＝收集器只存了部分紀錄，archivée／Opinion 判為無效）。
  1. 概覽表市場狀態列：事實是 Marketed、頁面寫成註銷／未上市類 → 標準句
       完整：「上市中（有效許可證：v／共 n）」；部分紀錄：「上市中（有效許可證：至少 v）」
  2. 張數列（概覽表緊接市場狀態列的下一列）：值含註銷字樣或數字與事實不符 → 「n（有效：v）」；部分紀錄 →「至少 n（有效：至少 v）」
  3. 許可證表：第一欄是證據包裡的許可證號、該證有效、列內有註銷字樣 → 只把註銷字樣換成該語言的「有效」
不改：front matter、散文（另案用模型）、事實不是 Marketed 的頁、br 資料不完整 8 頁。
輸出 .claude/audit_20261016/track5v2/：<站>.diff、summary.tsv、unmatched.tsv（找不到概覽列或張數列）
用法：python3 .claude/rewrite_market_v2_20261021.py [--apply] [站 ...]
"""
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / ".claude/audit_20261016/track5v2"
LANG = {"ARTxGNN": "es", "COTxGNN": "es", "ESTxGNN": "es", "BrTxGNN": "pt", "CHTxGNN": "de", "DETxGNN": "de",
        "DkTxGNN": "da", "FITxGNN": "fi", "FRTxGNN": "fr", "HkTxGNN": "zh", "TwTxGNN": "zh", "ITTxGNN": "it",
        "JpTxGNN": "ja", "KrTxGNN": "ko", "MyTxGNN": "ms", "NlTxGNN": "nl", "NOTxGNN": "no", "SATxGNN": "ar",
        "SETxGNN": "sv", "ThTxGNN": "th", "UsTxGNN": "en-us", "PhTxGNN": "en-us", "CaTxGNN": "en-us"}
T = {  # (完整, 部分, 張數完整, 張數部分)
    "en": ("Marketed (valid licences: {v} of {n})", "Marketed (valid licences on record: at least {v})", "{n} (valid: {v})", "at least {n}"),
    "en-us": ("Marketed (valid licenses: {v} of {n})", "Marketed (valid licenses on record: at least {v})", "{n} (valid: {v})", "at least {n}"),
    "es": ("Comercializado (registros vigentes: {v} de {n})", "Comercializado (registros vigentes: al menos {v})", "{n} (vigentes: {v})", "al menos {n}"),
    "pt": ("Comercializado (registros ativos: {v} de {n})", "Comercializado (registros ativos: pelo menos {v})", "{n} (ativos: {v})", "pelo menos {n}"),
    "de": ("Im Handel (gültige Zulassungen: {v} von {n})", "Im Handel (gültige Zulassungen: mindestens {v})", "{n} (gültig: {v})", "mindestens {n}"),
    "da": ("Markedsført (gyldige tilladelser: {v} af {n})", "Markedsført (gyldige tilladelser: mindst {v})", "{n} (gyldige: {v})", "mindst {n}"),
    "fi": ("Markkinoilla (voimassa olevia lupia: {v}/{n})", "Markkinoilla (voimassa olevia lupia: vähintään {v})", "{n} (voimassa: {v})", "vähintään {n}"),
    "fr": ("Commercialisé (autorisations valides : {v} sur {n})", "Commercialisé (autorisations valides : au moins {v})", "{n} (valides : {v})", "au moins {n}"),
    "zh": ("上市中（有效許可證 {v} 張／共 {n} 張）", "上市中（有效許可證至少 {v} 張）", "{n} 張（有效 {v} 張）", "至少 {n} 張"),
    "it": ("In commercio (autorizzazioni valide: {v} su {n})", "In commercio (autorizzazioni valide: almeno {v})", "{n} (valide: {v})", "almeno {n}"),
    "ja": ("販売中（有効な承認 {v} 件／全 {n} 件）", "販売中（有効な承認 {v} 件以上）", "{n} 件（有効 {v} 件）", "{n} 件以上"),
    "ko": ("시판 중 (유효 허가 {v}건 / 전체 {n}건)", "시판 중 (유효 허가 최소 {v}건)", "{n}건 (유효 {v}건)", "최소 {n}건"),
    "ms": ("Dipasarkan (pendaftaran sah: {v} daripada {n})", "Dipasarkan (pendaftaran sah: sekurang-kurangnya {v})", "{n} (sah: {v})", "sekurang-kurangnya {n}"),
    "nl": ("In de handel (geldige vergunningen: {v} van {n})", "In de handel (geldige vergunningen: minstens {v})", "{n} (geldig: {v})", "minstens {n}"),
    "no": ("Markedsført (gyldige tillatelser: {v} av {n})", "Markedsført (gyldige tillatelser: minst {v})", "{n} (gyldige: {v})", "minst {n}"),
    "ar": ("مُسوَّق (التراخيص السارية: {v} من {n})", "مُسوَّق (التراخيص السارية: {v} على الأقل)", "{n} (السارية: {v})", "{n} على الأقل"),
    "sv": ("Marknadsförd (giltiga godkännanden: {v} av {n})", "Marknadsförd (giltiga godkännanden: minst {v})", "{n} (giltiga: {v})", "minst {n}"),
    "th": ("วางจำหน่าย (ทะเบียนที่ยังมีผล {v} จาก {n} รายการ)", "วางจำหน่าย (ทะเบียนที่ยังมีผลอย่างน้อย {v} รายการ)", "{n} รายการ (ยังมีผล {v})", "อย่างน้อย {n} รายการ"),
}
# 許可證表：註銷字樣 → 有效（長的先換）
VALID_WORD = {
    "en": [("Cancelled", "Valid"), ("cancelled", "valid"), ("Canceled", "Valid"), ("canceled", "valid")],
    "es": [("Cancelado", "Vigente"), ("cancelado", "vigente"), ("Cancelada", "Vigente"), ("cancelada", "vigente")],
    "pt": [("Cancelado", "Ativo"), ("cancelado", "ativo"), ("Inativo", "Ativo")],
    "de": [("Erloschen", "Gültig"), ("erloschen", "gültig"), ("Widerrufen", "Gültig"), ("widerrufen", "gültig"), ("Zurückgezogen", "Gültig"), ("zurückgezogen", "gültig"), ("Aufgehoben", "Gültig"), ("aufgehoben", "gültig")],
    "da": [("Afmeldt", "Gyldig"), ("afmeldt", "gyldig"), ("Tilbagekaldt", "Gyldig"), ("tilbagekaldt", "gyldig")],
    "fi": [("Peruttu", "Voimassa"), ("peruttu", "voimassa")],
    "fr": [("AMM annulée", "AMM active"), ("AMM annulee", "AMM active"), ("Annulée", "Active"), ("annulée", "active"), ("Annulee", "Active"), ("annulee", "active"), ("AMM abrogée", "AMM active"), ("Abrogée", "Active"), ("abrogée", "active")],
    "zh": [("已註銷", "有效"), ("註銷", "有效"), ("已撤銷", "有效")],
    "it": [("Cancellata", "Valida"), ("cancellata", "valida"), ("Revocata", "Valida"), ("revocata", "valida"),
           ("Annullata", "Valida"), ("annullata", "valida"), ("Cessata", "Valida"), ("cessata", "valida")],
    "ja": [("取り消し済み", "有効"), ("取消済み", "有効"), ("取り消し", "有効"), ("取消", "有効"), ("整理済み", "有効"), ("失効", "有効")],
    "ko": [("취소됨", "유효"), ("취소", "유효")],
    "ms": [("Dibatalkan", "Sah"), ("dibatalkan", "sah")],
    "nl": [("Niet meer geregistreerd", "Geregistreerd"), ("niet meer geregistreerd", "geregistreerd"), ("Ingetrokken", "Geldig"), ("ingetrokken", "geldig"), ("Doorgehaald", "Geldig"), ("doorgehaald", "geldig"), ("geannuleerd", "geldig"), ("Vervallen", "Geldig"), ("vervallen", "geldig")],
    "no": [("Avregistrert", "Godkjent"), ("avregistrert", "godkjent"), ("Annullert", "Godkjent"), ("annullert", "godkjent"), ("Trukket tilbake", "Godkjent"), ("trukket tilbake", "godkjent"), ("trukket", "godkjent"), ("Tilbakekalt", "Godkjent"), ("tilbakekalt", "godkjent")],
    "ar": [("ملغى", "ساري"), ("ملغي", "ساري")],
    "sv": [("Avregistrerad", "Godkänd"), ("avregistrerad", "godkänd"), ("Avregistrerat", "Godkänt"), ("avregistrerat", "godkänt"), ("Återkallat", "Godkänt"), ("återkallat", "godkänt"), ("annullerat", "godkänt"), ("Annullerat", "Godkänt"), ("Återkallad", "Godkänd"), ("återkallad", "godkänd")],
    "th": [("ยกเลิกแล้ว", "ยังมีผล"), ("ยกเลิก", "ยังมีผล")],
}
VALID_WORD["en-us"] = VALID_WORD["en"]
LABEL = re.compile(r"market|markt|mercado|marché|marche|mercato|markkina|marknad|marked|status i norge|status i danmark|市販|上市|시판|pasaran|السوق|التسويق|การวางจำหน่าย", re.I)
# 許可證表只看「註銷」類字樣；not recorded／not found 在表裡是說適應症文字缺，不是許可證狀態
TABLE_NEG = None
NOT_MKT = {"en": "Approved but not marketed (approvals on record: {n})", "en-us": "Approved but not marketed (approvals on record: {n})",
           "es": "Autorizado pero no comercializado (registros: {n})"}
# pm A8：uk 的 license_id 是 NHS BNF 處方代碼（含 Spec 無許可特製品）、in 是市售商品清單，都不是許可證
RELABEL = {"UkTxGNN": [("Number of Marketing Authorisations", "Number of NHS prescribing items (BNF)"),
                       ("Marketing Authorisation Number", "BNF code")],
           "InTxGNN": [("Number of Registrations", "Number of marketed products"),
                       ("Authorization Number", "Product ID")]}
SKIP_TW = {"benzylpenicillin", "flucloxacillin", "nitrofurantoin", "procaine"}
COUNT_LABEL = re.compile(r"許可證數|件数|数$|數|antall|antal|number|nombre|número|numero|anzahl|lukumäärä|määrä|aantal|수|bilangan|عدد|จำนวน|tillatelser|godkjenninger|autorisasjoner", re.I)
NEG = re.compile(r"cancel|revok|withdraw|not marketed|not recorded|not found|unconfirmed|not confirmed|not populated|"
                 r"\b0 (licen|authori|registr|NDA)|cancelad|\banulad[ao]s?\b|retirad|no comercializad|sin registro|não comercializad|"
                 r"\binativ[oa]s?\b|widerruf|zurückgez|erloschen|nicht (im handel|vermarktet|zugelassen)|keine gültige|\bannul|retiré|"
                 r"non commercialis|\babrog|revocat|ritirat|non commercializzat|afmeld|ikke markedsført|ingen gyldig|tilbakekall|"
                 r"avregistr|inte marknadsförd|återkall|ingetrokken|niet in de handel|doorgehaald|vervallen|peruttu|"
                 r"ei markkinoilla|lakkautet|\bcessat[aeio]\b|\btrukket\b|aufgehoben|整理済み|失効|niet meer geregistreerd|取消|取り消|註銷|撤銷|未上市|販売中の承認なし|취소|미시판|tidak dipasarkan|dibatalkan|"
                 r"ملغى|ملغي|ملغاة|غير مسوق|أُلغيت|ألغيت|ยกเลิก|ไม่มีจำหน่าย|販売なし|未承認|non in commercio|afregistr|não é|não tem|não está", re.I)


TABLE_NEG = re.compile(NEG.pattern.replace(r"not recorded|not found|unconfirmed|not confirmed|not populated|", "").replace(r"\b0 (licen|authori|registr|NDA)|zero (licen|authori)|", "").replace(r"\b0 (licen|authori|registr|NDA)|", ""), re.I)


def norm_id(s):
    return re.sub(r"[\s*_`\[\]]", "", unicodedata.normalize("NFKC", s or "")).lower()


def indexable(t):
    return 'http-equiv="refresh"' not in t[:3000] and not re.search(r"^noindex:\s*true", t[:3000], re.M)


def main(argv):
    apply_ = "--apply" in argv
    sites = [a for a in argv if not a.startswith("--")] or sorted(p.name for p in BASE.glob("*TxGNN"))
    OUT.mkdir(parents=True, exist_ok=True)
    summary, unmatched, notes_miss, approved_nm, relabel_pages = [], [], [], [], []
    for s in sites:
        ff = BASE / ".claude/cache/license_facts" / f"{s}.json"
        if not ff.exists():
            print(f"✗ {s}: 沒有事實檔"); continue
        facts = json.loads(ff.read_text(encoding="utf-8"))
        lang = LANG.get(s, "en")
        full, part, cnt_full, cnt_part = T[lang]
        diffs, c = [], {"pages": 0, "status": 0, "count": 0, "table": 0, "partial_pages": 0}
        for f in sorted((BASE / s / "docs/_drugs").glob("*.md")):
            raw = f.read_bytes().decode("utf-8")
            crlf = "\r\n" in raw[:500]
            t = raw.replace("\r\n", "\n")
            if not indexable(t):
                continue
            fa = next((facts[k] for k in (f.stem, f.stem.replace("-", "_")) if k in facts), None)
            if s == "KrTxGNN":
                continue  # pm A8：kr 原始資料沒有取消欄位，市場狀態未知，不改寫
            if s in RELABEL:
                relabel_pages.append((s, f))
            if fa and fa.get("market_status") == "Approved, not marketed":
                lines0 = t.split("\n"); i0 = None
                fe = next(i for i in range(1, len(lines0)) if lines0[i] == "---")
                for k0 in range(fe + 1, len(lines0)):
                    c0 = lines0[k0].split("|")
                    if lines0[k0].startswith("|") and len(c0) >= 4 and LABEL.search(c0[1]) and not COUNT_LABEL.search(c0[1].strip()):
                        i0 = k0; break
                if i0 is not None and NEG.search(lines0[i0].split("|")[2]):
                    c0 = lines0[i0].split("|"); c0[2] = " " + NOT_MKT.get(lang, NOT_MKT["en"]).format(n=len(fa["licenses"])) + " "
                    lines0[i0] = "|".join(c0); t2 = "\n".join(lines0)
                    approved_nm.append((s, f.stem)); c["status"] += 1; c["pages"] += 1
                    diffs += difflib.unified_diff(t.splitlines(True), t2.splitlines(True), f"a/{s}/docs/_drugs/{f.name}", f"b/{s}/docs/_drugs/{f.name}", n=0)
                    if apply_:
                        f.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
                continue
            if not fa or fa.get("error") or fa.get("market_status") != "Marketed":
                continue
            if s == "BrTxGNN" and fa.get("valid", 0) == 0:
                continue
            if s == "TwTxGNN" and f.stem in SKIP_TW:
                continue  # 張數不是來自證據包（pm 2026-10-21），不改
            lines = t.split("\n")
            fm_end = next(i for i in range(1, len(lines)) if lines[i] == "---")
            n, v, partial = fa.get("total") or len(fa["licenses"]), fa["valid"], fa["partial"]
            changed = False
            # 1, 2：概覽表（本文第一個表格）
            first = next((i for i in range(fm_end + 1, len(lines)) if lines[i].startswith("|")), None)
            mi = None
            if first is not None:
                k = first
                while k < len(lines) and lines[k].startswith("|"):
                    cells = lines[k].split("|")
                    if mi is None and len(cells) >= 4 and LABEL.search(cells[1]) and not COUNT_LABEL.search(cells[1].strip()):
                        mi = k
                    k += 1
            if mi is None:
                if NEG.search("\n".join(lines[fm_end + 1:])):
                    unmatched.append((s, f.stem, "找不到概覽表市場狀態列"))
            else:
                cells = lines[mi].split("|")
                hit = [x for x in range(2, len(cells) - 1) if NEG.search(cells[x])]  # 有些頁的值欄重複兩次
                if hit:
                    for x in hit:
                        cells[x] = " " + (part.format(v=v) if partial else full.format(v=v, n=n)) + " "
                    lines[mi] = "|".join(cells); c["status"] += 1; changed = True
                # 張數列：同一個概覽表裡依標籤找（不靠位置；no、de 的張數列不一定緊接狀態列）
                status_fixed = lines[mi] != t.split("\n")[mi]
                ci = next((k for k in range(first, len(lines)) if lines[k].startswith("|") and k != mi
                           and COUNT_LABEL.search(lines[k].split("|")[1].strip()) and len(lines[k].split("|")) >= 4), None) if status_fixed else None
                if ci is not None and all(lines[x].startswith("|") for x in range(min(ci, mi), max(ci, mi) + 1)):
                    cc = lines[ci].split("|")
                    nums = [int(x) for x in re.findall(r"\d+", cc[2])]
                    want = (cnt_part.format(n=len(fa["licenses"]), v=v) if partial else cnt_full.format(n=n, v=v))
                    if cc[2].strip() != want:  # 狀態列已改正 → 張數列一律對齊同一組事實（不靠註銷字彙比對，nl「geen geldig／geschrapt」）
                        cc[2] = " " + want + " "
                        lines[ci] = "|".join(cc); c["count"] += 1; changed = True
                elif status_fixed:
                    unmatched.append((s, f.stem, "市場狀態列已改，但概覽表裡找不到張數列"))
                # nz propafenone 這類壞列：欄數多於表頭就裁掉多出來的欄
                hdr = lines[first].count("|")
                if lines[mi].count("|") > hdr:
                    lines[mi] = "|".join(lines[mi].split("|")[:hdr]) + "|"; changed = True
            # 3：許可證表
            valid_ids = {norm_id(k) for k, st in fa["licenses"].items() if st == "valid"}
            for j in range(fm_end + 1, len(lines)):
                l = lines[j]
                if not l.startswith("|") or j == mi:
                    continue
                cid = norm_id(l.split("|")[1]) if l.count("|") >= 3 else ""
                cid = re.sub(r"\(.*$", "", cid)
                if cid and cid in valid_ids and TABLE_NEG.search(l):
                    cells = l.split("|")
                    for x in range(1, len(cells) - 1):  # 第一欄也看（「字號 (cancelled)」同格），但第一欄只逐字替換
                        cell = cells[x]
                        if not TABLE_NEG.search(cell):
                            continue
                        for a, b in VALID_WORD[lang]:
                            cell = cell.replace(a, b)
                        cell = re.sub(r"(\w+)\s*[（(]\1[)）]", r"\1", cell, flags=re.I)  # Geldig (geldig) → Geldig
                        cell = re.sub(r"(\w+)\s*[・/、,]\s*\1\b", r"\1", cell, flags=re.I)  # 有効・有効、gültig/gültig → 單一
                        if TABLE_NEG.search(cell):
                            residue = re.sub(r"[\W_\d]+", "", re.sub(TABLE_NEG.pattern + "|" + "|".join(re.escape(b) for _, b in VALID_WORD[lang])
                                                                    + r"|status|estado|statut|stato|tila|状態|狀態|상태", "", cell, flags=re.I))
                            if x >= 2 and residue == "":  # 純狀態格（失効・取消）→ 整格改成有效字樣；混合格不動、列出
                                cell = " " + VALID_WORD[lang][0][1] + " "
                            else:
                                unmatched.append((s, f.stem, f"許可證表第 {j + 1} 行換字後仍有註銷字樣（未改）"))
                                cell = cells[x]
                        cells[x] = cell
                    new = "|".join(cells)
                    if new != l:
                        lines[j] = new; c["table"] += 1; changed = True
            if changed:
                t2 = "\n".join(lines)
                c["pages"] += 1; c["partial_pages"] += partial
                diffs += difflib.unified_diff(t.splitlines(True), t2.splitlines(True), f"a/{s}/docs/_drugs/{f.name}", f"b/{s}/docs/_drugs/{f.name}", n=0)
                if apply_:
                    f.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
                    # 同步寫進 notes（頁面本文＝notes；只改 docs 的話，下次 sync_notes_to_docs 會蓋回去）
                    nb = next((BASE / s / "data/notes" / k / "drug_pharmacist_notes.md" for k in (f.stem, f.stem.replace("-", "_"))
                               if (BASE / s / "data/notes" / k / "drug_pharmacist_notes.md").exists()), None)
                    if nb:
                        nt = nb.read_text(encoding="utf-8")
                        for a_, b_ in zip(t.split("\n"), t2.split("\n")):
                            if a_ != b_ and nt.count(a_) == 1:
                                nt = nt.replace(a_, b_)
                            elif a_ != b_ and a_.startswith(("monitor_inn", "predicted_", "indication_count", "description")) is False:
                                notes_miss.append((s, f.stem, a_[:80]))
                        nb.write_text(nt, encoding="utf-8")
        (OUT / f"{s}.diff").write_text("".join(diffs), encoding="utf-8")
        summary.append((s, c["pages"], c["status"], c["count"], c["table"], c["partial_pages"]))
        print(f"{s}: 改 {c['pages']} 頁（狀態列 {c['status']}、張數列 {c['count']}、許可證表 {c['table']} 列；其中部分紀錄 {c['partial_pages']} 頁）", flush=True)
    prev = {}
    if (OUT / "summary.tsv").exists():  # 與上一版對照每站表列數，避免無聲退步
        for line in (OUT / "summary.tsv").read_text(encoding="utf-8").splitlines()[1:]:
            c_ = line.split("\t")
            if len(c_) >= 5 and c_[4].isdigit():
                prev[c_[0]] = c_[4]
    (OUT / "summary.tsv").write_text("site\tpages\tstatus_rows\tcount_rows\ttable_rows\tpartial_pages\ttable_rows_prev\n" +
                                     "".join("\t".join(map(str, r)) + "\t" + prev.get(r[0], "") + "\n" for r in summary), encoding="utf-8")
    (OUT / "unmatched.tsv").write_text("site\tpage\treason\n" + "".join("\t".join(r) + "\n" for r in unmatched), encoding="utf-8")
    # uk／in 標籤改名（頁面與 notes 同步）
    nrel = 0
    rel_diff = []
    for s, f in relabel_pages:
        for path in (f, *[BASE / s / "data/notes" / k / "drug_pharmacist_notes.md" for k in (f.stem, f.stem.replace("-", "_"))]):
            if not path.exists():
                continue
            x = path.read_text(encoding="utf-8"); y = x
            for a_, b_ in RELABEL[s]:
                y = re.sub(r"(?m)^\|\s*" + re.escape(a_) + r"\s*\|", "| " + b_ + " |", y)
            if y != x:
                nrel += 1
                if path == f:
                    rel_diff.extend(difflib.unified_diff(x.splitlines(True), y.splitlines(True), f"a/{s}/docs/_drugs/{f.name}", f"b/{s}/docs/_drugs/{f.name}", n=0))
                if apply_:
                    path.write_text(y, encoding="utf-8")
    (OUT / "relabel_uk_in.diff").write_text("".join(rel_diff), encoding="utf-8")
    print(f"uk／in 標籤改名 {nrel} 檔；核准但未上市 {len(approved_nm)} 頁", flush=True)
    (OUT / "approved_not_marketed.tsv").write_text("site\tpage\n" + "".join(f"{a}\t{b}\n" for a, b in approved_nm), encoding="utf-8")
    (OUT / "notes_miss.tsv").write_text("site\tpage\tline\n" + "".join("\t".join(map(str, r)) + "\n" for r in notes_miss), encoding="utf-8")
    print("合計", [sum(r[i] for r in summary) for i in range(1, 6)], "對不到", len(unmatched))


if __name__ == "__main__":
    main(sys.argv[1:])
