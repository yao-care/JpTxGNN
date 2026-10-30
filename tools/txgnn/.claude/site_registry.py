#!/usr/bin/env python3
"""
30 國 TxGNN 站台的權威資料表。

setup_country.sh、gen_standard_pages.py、patch_existing_content.py、
set_repo_about.py、p0 檢查共用這一份，避免各腳本各自硬編一套國名與主管機關而漂移。

欄位說明：
    lang         docs/_config.yml 的 lang（實查，非推測）
    country      該站涵蓋的國家／地區（英文）
    country_zh   國家／地區的中文名，給中文站的正文用
    agency       藥證主管機關簡稱（英文）
    agency_zh    主管機關中文名。只有中文站（Tw / Hk）會用到，
                 其餘站沿用英文縮寫即可——那些站不產中文正文。
    agency_url   主管機關官網
    content_lang 產生頁面時採用的語言：en / zh-Hant
                 非這兩者的站先產英文骨架，再由翻譯流程換成母語。

主管機關來源：各站 docs/index.md 與 README.md 的既有敘述（2026-07-25 實查）。
"""

# proj -> (lang, country, country_zh, agency, agency_zh, agency_url, content_lang)
SITES = {
    "ARTxGNN": ("es", "Argentina", "阿根廷", "ANMAT", "ANMAT", "https://www.argentina.gob.ar/anmat", "es"),
    "AuTxGNN": ("en-AU", "Australia", "澳洲", "TGA", "TGA", "https://www.tga.gov.au/", "en"),
    "BrTxGNN": ("pt-BR", "Brazil", "巴西", "ANVISA", "ANVISA", "https://www.gov.br/anvisa/", "pt"),
    "CaTxGNN": ("en-CA", "Canada", "加拿大", "Health Canada", "Health Canada", "https://www.canada.ca/en/health-canada.html", "en"),
    "CHTxGNN": ("de", "Switzerland", "瑞士", "Swissmedic", "Swissmedic", "https://www.swissmedic.ch/", "de"),
    "COTxGNN": ("es-CO", "Colombia", "哥倫比亞", "INVIMA", "INVIMA", "https://www.invima.gov.co/", "es"),
    "DETxGNN": ("de", "Germany", "德國", "BfArM", "BfArM", "https://www.bfarm.de/", "de"),
    "DkTxGNN": ("da", "Denmark", "丹麥", "DKMA", "DKMA", "https://laegemiddelstyrelsen.dk/", "da"),
    "ESTxGNN": ("es", "Spain", "西班牙", "AEMPS", "AEMPS", "https://www.aemps.gob.es/", "es"),
    "EuTxGNN": ("en", "the European Union", "歐盟", "EMA", "EMA", "https://www.ema.europa.eu/", "en"),
    "FITxGNN": ("fi", "Finland", "芬蘭", "Fimea", "Fimea", "https://fimea.fi/", "fi"),
    "FRTxGNN": ("fr", "France", "法國", "ANSM", "ANSM", "https://ansm.sante.fr/", "fr"),
    "HkTxGNN": ("zh-Hant-HK", "Hong Kong", "香港", "Department of Health HK", "衛生署藥物辦公室", "https://www.drugoffice.gov.hk/", "zh-Hant"),
    "InTxGNN": ("en", "India", "印度", "CDSCO", "CDSCO", "https://cdsco.gov.in/", "en"),
    "ITTxGNN": ("it", "Italy", "義大利", "AIFA", "AIFA", "https://www.aifa.gov.it/", "it"),
    "JpTxGNN": ("ja", "Japan", "日本", "PMDA", "PMDA", "https://www.pmda.go.jp/", "ja"),
    "KrTxGNN": ("ko", "South Korea", "韓國", "MFDS", "MFDS", "https://www.mfds.go.kr/", "ko"),
    "MyTxGNN": ("ms", "Malaysia", "馬來西亞", "NPRA", "NPRA", "https://npra.gov.my/", "ms"),
    "NlTxGNN": ("nl", "the Netherlands", "荷蘭", "CBG-MEB", "CBG-MEB", "https://www.cbg-meb.nl/", "nl"),
    "NOTxGNN": ("no", "Norway", "挪威", "DMP", "DMP", "https://www.dmp.no/", "no"),
    "NZTxGNN": ("en-NZ", "New Zealand", "紐西蘭", "Medsafe", "Medsafe", "https://www.medsafe.govt.nz/", "en"),
    "PhTxGNN": ("en", "the Philippines", "菲律賓", "FDA Philippines", "FDA Philippines", "https://www.fda.gov.ph/", "en"),
    "SATxGNN": ("ar", "Saudi Arabia", "沙烏地阿拉伯", "SFDA", "SFDA", "https://www.sfda.gov.sa/", "ar"),
    "SETxGNN": ("sv", "Sweden", "瑞典", "MPA", "MPA", "https://www.lakemedelsverket.se/", "sv"),
    "SgTxGNN": ("en-SG", "Singapore", "新加坡", "HSA", "HSA", "https://www.hsa.gov.sg/", "en"),
    "ThTxGNN": ("th", "Thailand", "泰國", "Thai FDA", "Thai FDA", "https://www.fda.moph.go.th/", "th"),
    "TwTxGNN": ("zh-Hant", "Taiwan", "台灣", "TFDA", "食藥署 TFDA", "https://www.fda.gov.tw/", "zh-Hant"),
    "UkTxGNN": ("en-GB", "the United Kingdom", "英國", "MHRA", "MHRA", "https://www.gov.uk/mhra", "en"),
    "UsTxGNN": ("en", "the United States", "美國", "FDA", "FDA", "https://www.fda.gov/", "en"),
    "ZaTxGNN": ("en", "South Africa", "南非", "SAHPRA", "SAHPRA", "https://www.sahpra.org.za/", "en"),
}

FIELDS = ("lang", "country", "country_zh", "agency", "agency_zh", "agency_url", "content_lang")


def get(proj: str) -> dict:
    """回傳站台資料 dict；未登錄的站台丟 KeyError，不猜。"""
    return dict(zip(FIELDS, SITES[proj]))


def all_projects() -> list[str]:
    return sorted(SITES)
