"""許可證排程更新（2026-10-29，用戶：各站 repo 自己在 GitHub 定期更新許可證並 merge main）。全程不用 AI。

在 scripts/txgnn_ws.sh 組出的工作目錄裡跑（BASE＝工作目錄，BASE/<站>＝站 repo）。站專屬的下載與對應寫在
<站>/scripts/license_adapter.py（介面見 load_adapter）。pm 驗收條件（2026-10-29）逐條對應：
  1 不經 AI：本支與它呼叫的腳本都不呼叫模型；有設 ALLOW_AI_REGEN 直接中止
  2 先停損：這輪改到的藥物頁 > min(200, 該站藥物頁 5%) → 不寫回、exit 3；checker 非 0、gate、h1 沒過 → exit 4
    只改許可證欄位（狀態列、張數列、許可證表狀態格）；改到表格列以外的行 → 整批還原、exit 4
  3 lastmod：正文真的有變才換成今天；只動到 front matter 的頁還原成原本的 last_modified_at
  4 有人工查核紀錄（docs/_data/drug_reviews.json）的頁被改到 → 還原這些頁、exit 5，等人簽核
  5 下載失敗或格式變了 → exit 2，一頁都不改（下載不到的許可證保留原狀態，不寫成未記載）
  6 排程時間與 push 前 pull --rebase 在 workflow
結果寫 <站>/.license_refresh/summary.json 與 summary.md（workflow 拿來開 issue／寫 run summary）。
用法（工作目錄）：python3 .claude/license_refresh_20261029.py 站 [--dry-run]
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TPE = timezone(timedelta(hours=8))
PY = sys.executable


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def load_adapter(site):
    """站上的 scripts/license_adapter.py 要提供：
       RAW_FILE                     data/ 下的原始快照相對路徑（下載成功才覆寫）
       fetch() -> list[dict]        從主管機關下載全部許可證；失敗就 raise
       validate(new, old) -> list[str]  格式／數量檢查，回傳問題（空＝通過）；old 是上次快照（可能 None）
       status_index(new) -> dict    {許可證號: 新狀態 dict}
       record_id(rec) -> str        bundle tfda.records 一筆的許可證號
       update(rec, new) -> bool     依新狀態改這筆紀錄，有改回 True
    """
    return _load("license_adapter", BASE / site / "scripts/license_adapter.py")


def run(cmd, cwd=BASE, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(map(str, cmd))} 失敗：{(r.stderr or r.stdout)[-800:]}")
    return r


def git(site, *a):
    return run(["git", *a], cwd=BASE / site, check=False).stdout


def changed_drug_pages(site):
    return sorted(l[3:].strip() for l in git(site, "status", "--porcelain", "--", "docs/_drugs").split("\n") if l.strip().endswith(".md"))


def fix_lastmod(site, today):
    """正文有變→今天；只有 front matter 變→還原原本的 last_modified_at（pm 第 3 條）"""
    lm = _load("lm", BASE / ".claude/lastmod_fix_20261029.py")
    n_body = 0
    for rel in changed_drug_pages(site):
        p = BASE / site / rel
        old = run(["git", "show", f"HEAD:{rel}"], cwd=BASE / site, check=False).stdout
        raw = p.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw[:500]
        t = raw.replace("\r\n", "\n")
        m_old = re.search(r"^last_modified_at:.*$", old.replace("\r\n", "\n"), re.M)
        if lm.body(old) != lm.body(t):
            n_body += 1
            new_line = f"last_modified_at: {today}"
        elif m_old:
            new_line = m_old.group(0)
        else:
            continue
        t2 = re.sub(r"^last_modified_at:.*$", new_line, t, count=1, flags=re.M) if re.search(r"^last_modified_at:", t, re.M) else t
        if t2 != t:
            p.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
    return n_body


def main(argv):
    site = next(a for a in argv if a.endswith("TxGNN"))
    dry = "--dry-run" in argv
    out = BASE / site / ".license_refresh"
    out.mkdir(exist_ok=True)
    S = {"site": site, "date": datetime.now(TPE).strftime("%Y-%m-%d"), "steps": []}

    def finish(code, msg):
        S["exit"], S["result"] = code, msg
        (out / "summary.json").write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        md = [f"## {site} 許可證更新 {S['date']}：{msg}", ""] + [f"- {x}" for x in S["steps"]]
        if S.get("missing_alert"):
            md += ["", f"### 新資料查不到的許可證（超過 2%，前 300 張）", ""] + [f"- `{x}`" for x in S["not_in_source"]]
        if S.get("held"):
            md += ["", f"### 擋下、等人看的頁（{len(S['held'])}）", ""] + [f"- `{x}`" for x in S["held"]]
        if S.get("checker_bad"):
            md += ["", "### checker 非 0 的頁", ""] + [f"- `{x}`" for x in S["checker_bad"]]
        if S.get("to_verify"):
            md += ["", f"### 狀態列變成全部註銷／查無、要對全量來源依成分確認的頁（{len(S['to_verify'])}）", ""] + [f"- `{x}`" for x in S["to_verify"]]
        if S.get("unsynced"):
            md += ["", "### 本站沒有對應寫法、未改的許可證表格子", ""] + [f"- {x}" for x in S["unsynced"]]
        if S.get("fields"):
            md += ["", f"### 逐欄位變更（{len(S['fields'])}）", "", "| 頁 | 欄位 | 前值 → 後值 |", "|---|---|---|"] + \
                  ["| " + x.replace("｜", " | ", 2) + " |" for x in S["fields"][:600]]
        if S.get("pages"):
            md += ["", f"### 改到的藥物頁（{len(S['pages'])}）", ""] + [f"- `{x}`" for x in S["pages"][:300]]
        (out / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        print("\n".join(md))
        sys.exit(code)

    if os.environ.get("ALLOW_AI_REGEN"):
        finish(4, "環境設了 ALLOW_AI_REGEN，排程不准使用 AI 重生，中止")
    if changed_drug_pages(site):
        finish(4, "工作目錄已有未提交的藥物頁改動，中止（避免混入）")

    # 1. 下載與檢查：失敗一頁都不改
    ad = load_adapter(site)
    raw_path = BASE / site / "data" / ad.RAW_FILE
    old = json.loads(raw_path.read_text(encoding="utf-8")) if raw_path.exists() else None
    try:
        new = ad.fetch()
    except Exception as e:
        finish(2, f"下載失敗：{str(e)[:300]}")
    problems = ad.validate(new, old)
    if getattr(ad, "WATCH", False):
        # 監看模式（2026-10-30，PH／TH／IN：來源不會定期更新、或只能看發布頁）：比對來源指紋，有變就開 issue（exit 6），不改頁
        if problems:
            finish(2, "監看來源抓取有問題：" + "；".join(problems))
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        if old is None:
            raw_path.write_text(json.dumps(new, ensure_ascii=False, indent=1), encoding="utf-8")
            S["license_changes"] = ["watch-init"]
            finish(0, f"首次記錄來源指紋（{len(new)} 項），之後有變化會開 issue")
        if new == old:
            finish(0, f"來源沒有變化（{len(new)} 項）")
        S["license_changes"] = ["watch"]
        S["steps"].append(ad.describe(old, new) if hasattr(ad, "describe") else "來源內容有變")
        raw_path.write_text(json.dumps(new, ensure_ascii=False, indent=1), encoding="utf-8")
        finish(6, "來源有更新，請人工確認是否要更新本站資料（頁面未自動修改）")
    idx = ad.status_index(new)
    bundles = sorted((BASE / site / "data/bundles").glob("*/drug_bundle.json"))
    if not bundles:
        finish(2, "找不到 data/bundles（先跑 scripts/restore_data.sh）")
    lts = _load("lts", BASE / ".claude/license_table_sync_20261029.py")
    ids = {ad.record_id(r) for f in bundles for r in lts.reg_block(json.loads(f.read_text(encoding="utf-8"))).get("records", [])}
    ids.discard(None); ids.discard("")
    cover = sum(1 for i in ids if i in idx) / max(1, len(ids))
    S["steps"].append(f"下載 {len(new)} 筆（上次 {len(old) if old is not None else '無'} 筆）；證據包裡 {len(ids)} 張許可證，新資料涵蓋 {cover:.1%}")
    cmin = getattr(ad, "COVER_MIN", 0.95)
    S["not_in_source"] = sorted(i for i in ids if i not in idx)[:300]  # 新資料查不到的許可證：保留原狀態，只列出來
    if S["not_in_source"]:
        n_miss = sum(1 for i in ids if i not in idx)
        S["steps"].append(f"新資料查不到 {n_miss} 張許可證（保留原狀態，不推定為撤銷）")
        S["missing_alert"] = n_miss / max(1, len(ids)) > (1 - cmin) + 0.02 if cmin < 0.95 else n_miss / max(1, len(ids)) > 0.02  # 超過基準 2% 開 issue（pm 2026-10-30）
    # cmin：站專屬涵蓋門檻（例：Za 匯出檔不含舊制藥品，見轉換器說明）
    if cover < cmin:
        problems.append(f"新資料只涵蓋證據包許可證的 {cover:.1%}（門檻 {cmin:.0%}），疑似格式或來源改變")
    if problems:
        finish(2, "資料檢查沒過：" + "；".join(problems))

    # 2a. 用「更新前的證據包」算一次事實，從現有頁面學各站許可證表狀態欄的寫法（license_table_sync）
    lts = _load("lts", BASE / ".claude/license_table_sync_20261029.py")
    if not dry:
        run([PY, ".claude/dump_license_facts_20261021.py", site])
        # 用語優先用固定檔（2026-10-30 在 Mac 從「頁面與事實一致」的狀態學出）；頁面落後於事實時現學會學歪
        lf = BASE / ".claude/license_labels" / f"{site}.json"
        labels = json.loads(lf.read_text(encoding="utf-8")) if lf.exists() else lts.learn(site)
        S["steps"].append(f"許可證表狀態欄寫法：{labels['preferred']}")

    # 2b. 寫回證據包（下載不到的許可證保留原狀態）
    n_rec, n_bundle, changes = 0, 0, []
    for f in bundles:
        b = json.loads(f.read_text(encoding="utf-8"))
        ch = bool(getattr(ad, "preprocess", None) and ad.preprocess(b))  # 站專屬的前處理（例：EMA 獸用許可移出）
        if ch:
            changes.append(f"{f.parent.name} preprocess 前處理")
        for r in lts.reg_block(b).get("records", []):
            nv = idx.get(ad.record_id(r))
            if nv is not None:
                before = r.get("status")
                if ad.update(r, nv):
                    ch = True; n_rec += 1; changes.append(f"{f.parent.name} {ad.record_id(r)} {before}→{r.get('status')}")
        if ch:
            n_bundle += 1
            if not dry:
                f.write_text(json.dumps(b, ensure_ascii=False, indent=2), encoding="utf-8")
    n_id = len({c.split(" ")[1] for c in changes if " preprocess " not in c})  # 同一張許可證在證據包裡可能重複多筆（例如 CO 每個包裝一筆）
    S["steps"].append(f"許可證狀態有變 {n_rec} 筆（{n_id} 張不重複許可證）、{n_bundle} 個藥")
    S["license_changes"] = changes[:1000]
    rmax = float(os.environ.get("LICENSE_REFRESH_MAX_CHANGE") or 0.2)  # 只給手動補跑（第一次換官方來源）用，排程不設
    if len(ids) and n_id / len(ids) > rmax:
        finish(2, f"狀態變動 {n_id}/{len(ids)} 張許可證超過 {rmax:.0%}，疑似來源格式改變，不寫回")
    if dry:
        finish(0, f"試跑：{n_rec} 筆狀態會變，未寫回")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(new, ensure_ascii=False, indent=2), encoding="utf-8")

    # 3. 只改許可證欄位（pm 2026-10-30 第 2 點）：概覽表本站狀態列、既有張數列、許可證表狀態格。
    #    不跑事實層、fix_residual、衍生檔重產——H1、原適應症、description、預測內容一律不動。
    #    證據包沒變也照跑：頁面若落後於事實（例如上次停在一半）會在這裡對齊。
    run([PY, ".claude/dump_license_facts_20261021.py", site])
    rows = lts.sync_market_rows(site)
    # 2026-10-31（pm）：狀態列這次變成「全部註銷／查無」的頁，要先對全量來源依成分確認才能算定案（證據包可能只收了部分登記號）；
    # 排程不自己判斷，列進 issue 給 pm 追蹤。已改寫成資料範圍句的站（SCOPE_CANCELLED／NO_CENTRAL）不列。
    ckm = _load("ckm", BASE / ".claude/check_drug_page.py")
    fs_now = lts.facts(site)
    scoped = {"Cancelled only": site in ckm.SCOPE_CANCELLED, "Not marketed": site in ckm.NO_CENTRAL}
    S["to_verify"] = sorted(pg for pg in rows if scoped.get((lts.page_facts(fs_now, pg) or {}).get("market_status"), True) is False)
    tch, unsynced = lts.apply(site, labels)
    tch += lts.drop_excluded_rows(site)
    fields = [(pg, lab, a_, b_) for pg, ch in rows.items() for lab, a_, b_ in ch] + tch
    S["fields"] = [f"{pg}｜{lab}｜{a_} → {b_}" for pg, lab, a_, b_ in fields]
    S["steps"].append(f"概覽表狀態／張數列改 {sum(len(v) for v in rows.values())} 格（{len(rows)} 頁）；許可證表狀態格改 {len(tch)} 格"
                      + (f"；本站沒有對應寫法、未改 {len(unsynced)} 格" if unsynced else ""))
    S["unsynced"] = unsynced[:200]
    if not changed_drug_pages(site):
        finish(0, "頁面上的許可證欄位已與最新資料一致，不改頁")

    # 3b. 自我檢查：每頁改到的行只能是表格列（狀態列、張數列、許可證表），否則整批還原
    for rel in changed_drug_pages(site):
        old_t = run(["git", "show", f"HEAD:{rel}"], cwd=BASE / site, check=False).stdout.replace("\r\n", "\n").split("\n")
        new_t = (BASE / site / rel).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
        import difflib
        bad_l = [l for l in difflib.unified_diff(old_t, new_t, lineterm="", n=0)
                 if l[:1] in "+-" and not l.startswith(("+++", "---")) and not l[1:].startswith("|")]
        if bad_l:
            S["pages"] = [rel]
            git(site, "checkout", "--", "docs")
            finish(4, f"{rel} 有表格列以外的改動（{bad_l[0][:80]}），整批還原")

    # 3c. checker 全量必須 0；不自動刪句修補，非 0 就還原、開 issue
    ck = run([PY, ".claude/checker_trend.py", "--no-append", site], check=False).stdout
    m = re.search(r"非 0 (\d+)", ck)
    S["steps"].append("checker 全量：" + (ck.strip().split("\n")[0] if ck.strip() else "沒有輸出"))
    if not m or m.group(1) != "0":
        # 非 0 的頁單獨擋下（還原、列進 held，workflow 另開 issue 等人看），其餘頁照常；擋下後必須歸零
        det = re.search(r"明細 (\S+)", ck)
        bad = [l.split("\t") for l in (BASE / det.group(1)).read_text(encoding="utf-8").split("\n")[1:] if l.count("\t") == 3 and l.split("\t")[3]] if det else []
        S["checker_bad"] = ["\t".join(x) for x in bad][:100]
        held = [x[1] for x in bad]
        if not bad or len(held) > 20:
            S["pages"] = changed_drug_pages(site)
            git(site, "checkout", "--", "docs")
            finish(4, "checker 非 0，頁面已還原、不 merge（明細見 checker_bad）")
        for pg in held:
            git(site, "checkout", "--", f"docs/_drugs/{pg}.md")
        S["held"] = held
        S["fields"] = [x for x in S["fields"] if x.split("｜", 1)[0] not in held]
        ck = run([PY, ".claude/checker_trend.py", "--no-append", site], check=False).stdout
        det = re.search(r"明細 (\S+)", ck)
        rest = [l.split("\t")[1] for l in (BASE / det.group(1)).read_text(encoding="utf-8").split("\n")[1:]
                if l.count("\t") == 3 and l.split("\t")[3]] if det else ["?"]
        rest = [x for x in rest if x not in held]  # 擋下的頁維持舊版，本來就跟新事實對不上，已列入 issue
        S["steps"].append(f"擋下 {len(held)} 頁（頁面其他地方跟新狀態矛盾，排程不改正文，等人看）：{', '.join(held)}；其餘頁 checker 非 0：{len(rest)}")
        if rest:
            S["pages"] = changed_drug_pages(site)
            git(site, "checkout", "--", "docs")
            finish(4, "擋下非 0 頁後 checker 仍非 0，全部還原")

    # 4. 有人工查核紀錄的頁不自動改（Tw）
    rv = BASE / site / "docs/_data/drug_reviews.json"
    if rv.exists():
        prot = {r.get("drug") for r in json.loads(rv.read_text(encoding="utf-8")).get("records", [])}
        hit = [p for p in changed_drug_pages(site) if Path(p).stem in prot]
        if hit:
            S["pages"] = hit
            git(site, "checkout", "--", "docs")
            finish(5, f"{len(hit)} 個有人工查核紀錄的頁會被改到，全部還原，等用戶簽核")

    # 5. lastmod（正文有變才換日期）
    n_body = fix_lastmod(site, S["date"])
    pages = changed_drug_pages(site)
    S["pages"] = pages
    S["steps"].append(f"藥物頁有改 {len(pages)} 頁（正文有變 {n_body} 頁）")

    # 6. 停損門檻、gate、h1
    total = len(list((BASE / site / "docs/_drugs").glob("*.md")))
    limit = min(200, max(1, int(total * 0.05)))
    if os.environ.get("LICENSE_REFRESH_MAX_PAGES", "").isdigit():  # 只給手動觸發的補跑用（workflow input max_pages），排程不設
        limit = int(os.environ["LICENSE_REFRESH_MAX_PAGES"])
        S["steps"].append(f"手動放寬停損門檻為 {limit} 頁")
    if len(pages) > limit:
        git(site, "checkout", "--", "docs")
        finish(3, f"改到 {len(pages)} 頁，超過門檻 {limit}（min(200, 5%×{total})），不 merge，等人看")
    g = run([PY, "scripts/check_seo_docs.py"], cwd=BASE / site, check=False)
    if g.returncode != 0:
        S["steps"].append("gate 輸出：" + (g.stdout + g.stderr)[-600:])
        git(site, "checkout", "--", "docs")
        finish(4, "gate（check_seo_docs.py）沒過，頁面已還原")
    lc = _load("lc", BASE / ".claude/launch_commit_20261028.py")
    h1bad = [p for p in pages if lc.h1_count((BASE / site / p).read_text(encoding="utf-8")) != 1]
    if h1bad:
        S["pages"] = h1bad
        git(site, "checkout", "--", "docs")
        finish(4, f"{len(h1bad)} 頁 h1 不是恰好 1 個，頁面已還原")
    finish(0, f"可以 merge：改 {len(pages)} 頁，checker 0、gate 通過")


if __name__ == "__main__":
    main(sys.argv[1:])
