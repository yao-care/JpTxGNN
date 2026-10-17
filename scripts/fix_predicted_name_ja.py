"""「予測新適応症」欄的病名是繁體中文的頁，改成日本語の医学用語（括號內英文保留）（2026-10-17，T-314 追加）。
頁面與筆記一起改，只替換該欄的完整字串；報告本文其他中文段落屬 T-315（重譯），不在此處理。
用法：python3 scripts/fix_predicted_name_ja.py [--dry-run]
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = {
 "acebutolol": [("惡性腎血管高血壓", "悪性腎血管性高血圧")],
 "acetazolamide": [("心肌病變", "心筋症")],
 "acitretin": [("青春痘", "尋常性ざ瘡")],
 "alirocumab": [("黃色瘤病", "黄色腫症"), ("膽固醇分解代謝疾病", "コレステロール異化障害")],
 "alprostadil": [("主動脈畸形、先天性三尖瓣狹窄、心室中隔缺損", "大動脈奇形、先天性三尖弁狭窄症、心室中隔欠損症")],
 "aluminum_chloride": [("脂漏性角化症、脂漏性皮膚炎、痤瘡、皮膚疾病（多汗相關）", "脂漏性角化症、脂漏性皮膚炎、ざ瘡、皮膚疾患（多汗関連）")],
 "belimumab": [("血小板原發性釋放障礙", "血小板一次放出異常症")],
 "bempedoic_acid": [("同合子家族性高膽固醇血症", "ホモ接合体家族性高コレステロール血症")],
 "benzylpenicillin": [("牙冠周炎", "智歯周囲炎")],
 "brivaracetam": [("視覺性癲癇", "視覚性てんかん")],
 "brodalumab": [("眼病 (Eye Disease)", "眼疾患 (Eye Disease)")],
 "buprenorphine": [("急性間歇性紫質症", "急性間欠性ポルフィリン症")],
 "butenafine": [("皮膚念珠菌病", "皮膚カンジダ症")],
 "cisatracurium": [("子癲前症", "妊娠高血圧腎症")],
 "dronedarone": [("中風疾病", "脳卒中")],
 "dupilumab": [("支氣管炎", "気管支炎")],
 "human_immunoglobulin_g": [("糖尿病視網膜病變", "糖尿病網膜症")],
 "hydroxyprogesterone_caproate": [("子宮內膜癌", "子宮内膜癌")],
 "hydroxyurea": [("女性乳腺癌", "女性乳癌")],
 "ipratropium": [("阻塞性肺疾病", "閉塞性肺疾患")],
 "isosorbide_dinitrate": [("肺高壓 (pulmonary hypertension)、脫髮症 (alopecia)", "肺高血圧症 (pulmonary hypertension)、脱毛症 (alopecia)")],
 "minoxidil": [("頭皮單純性稀毛症", "頭皮単純性乏毛症")],
 "naftifine": [("皮膚念珠菌病、花斑癬、Majocchi 肉芽腫", "皮膚カンジダ症、癜風、Majocchi 肉芽腫")],
 "nystatin": [("外陰陰道炎", "外陰腟炎")],
 "omalizumab": [("支氣管炎、異位性皮膚炎", "気管支炎、アトピー性皮膚炎")],
 "oteracil": [("大腸腫瘤", "大腸腫瘍")],
 "pralatrexate": [("胸膜上皮型間皮瘤", "胸膜上皮型中皮腫")],
 "prednisolone_acetate": [("寄生蟲性結膜炎", "寄生虫性結膜炎")],
 "prednisone": [("圓禿症", "円形脱毛症")],
 "ribavirin": [("慢性 B 型肝炎病毒感染", "慢性 B 型肝炎ウイルス感染症")],
 "riluzole": [("雙側旁矢狀頂枕多小腦回畸形、下運動神經元症候群、Mills 症候群、ALS 易感性", "両側傍矢状頭頂後頭多小脳回、下位運動ニューロン症候群、Mills 症候群、ALS 感受性")],
 "ritonavir": [("猿免疫缺乏病毒感染", "サル免疫不全ウイルス感染症"), ("貓愛滋病", "ネコ後天性免疫不全症候群")],
 "salicylamide": [("普通感冒 (common cold)、咽炎 (pharyngitis)", "感冒 (common cold)、咽頭炎 (pharyngitis)")],
 "sodium_carbonate": [("過敏反應（anaphylaxis）、乾眼症（dry eye syndrome）", "アナフィラキシー（anaphylaxis）、ドライアイ（dry eye syndrome）")],
 "sodium_citrate": [("胃部疾病（stomach disease）", "胃疾患（stomach disease）")],
 "sulfamethazine": [("糖尿病腎病變（diabetic nephropathy）", "糖尿病性腎症（diabetic nephropathy）"), ("支氣管炎（bronchitis）", "気管支炎（bronchitis）")],
 "tetryzoline": [("鼻腔疾病", "鼻腔疾患")],
 "treprostinil": [("肺動脈高壓相關疾病（先天性心臟病、HIV 感染、結締組織疾病等）", "肺動脈性肺高血圧症関連疾患（先天性心疾患、HIV 感染症、結合組織病など）")],
 "trifluoperazine": [("躁鬱症躁症期", "双極性障害の躁病相")],
 "vinorelbine": [("Ewing 肉瘤", "Ewing 肉腫")],
 "vismodegib": [("著色性乾皮症", "色素性乾皮症")],
 "vitamin_e": [("先天性膽紅素代謝異常", "先天性ビリルビン代謝異常症")],
 "xylometazoline": [("鼻腔疾病、急性咽喉炎", "鼻腔疾患、急性咽喉頭炎")],
 "zanubrutinib": [("骨髓性白血病", "骨髄性白血病")],
}
ROW = re.compile(r"^(\|\s*予測新規?適応症\s*\|)([^|\n]+)(\|)", re.M)


def fix_text(t, pairs):
    m = ROW.search(t)
    if not m:
        return t, False
    cell = m.group(2)
    new = cell
    for a, b in pairs:
        new = new.replace(a, b)
    if new == cell:
        return t, False
    return t[:m.start(2)] + new + t[m.end(2):], True


def main(dry):
    n = 0
    for stem, pairs in FIX.items():
        for p in (ROOT / "docs/_drugs" / f"{stem}.md", ROOT / "data/notes" / stem / "drug_pharmacist_notes.md"):
            if not p.exists():
                continue
            t = p.read_text(encoding="utf-8")
            nt, ch = fix_text(t, pairs)
            if ch:
                n += 1
                if not dry:
                    p.write_text(nt, encoding="utf-8")
            elif p.parent.name == "_drugs":
                print("未替換", stem)
    print("更新檔案", n)


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
