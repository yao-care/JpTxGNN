#!/usr/bin/env python3
"""
新聞處理腳本

功能：
1. 讀取所有 data/news/*.json 來源檔案
2. 載入 keywords.json 進行關鍵字匹配
3. 跨站去重（相似標題合併來源）
4. 輸出 matched_news.json
5. 產生 docs/_news/*.md 頁面
"""

import json
import re
from datetime import datetime, timezone, timedelta
from difflib import SequenceMatcher
from pathlib import Path

# 專案根目錄
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "news"
DOCS_DIR = PROJECT_ROOT / "docs"
NEWS_COLLECTION_DIR = DOCS_DIR / "_news"

# 設定
SIMILARITY_THRESHOLD = 0.8  # 標題相似度閾值
TIME_WINDOW_HOURS = 24  # 去重時間窗口（小時）
MAX_NEWS_AGE_DAYS = 30  # 最大新聞保留天數


LANG_BY_PROJECT = {
    "ARTxGNN": "es", "AuTxGNN": "en", "BrTxGNN": "pt", "CaTxGNN": "en",
    "CHTxGNN": "de", "COTxGNN": "es", "DETxGNN": "de", "DkTxGNN": "da",
    "ESTxGNN": "es", "EuTxGNN": "en", "FITxGNN": "fi", "FRTxGNN": "fr",
    "HkTxGNN": "zh", "InTxGNN": "en", "ITTxGNN": "it", "JpTxGNN": "ja",
    "KrTxGNN": "ko", "MyTxGNN": "ms", "NlTxGNN": "nl", "NOTxGNN": "no",
    "NZTxGNN": "en", "PhTxGNN": "en", "SATxGNN": "ar", "SETxGNN": "sv",
    "SgTxGNN": "en", "ThTxGNN": "th", "TwTxGNN": "zh", "UkTxGNN": "en",
    "UsTxGNN": "en", "ZaTxGNN": "en",
}

NEWS_STRINGS = {
    "en": {
        "parent": "Health News",
        "title_news": "{name} News",
        "back": "← Back to News Overview",
        "q": "What news is there about {name}?",
        "sum_drug": "<strong>{name}</strong> currently has <strong>{n} news articles</strong>, with {m} predicted indications.",
        "take_drug": "This page combines the AI-predicted indications for {name} with the latest health news. Indications highlighted in orange have recent news coverage.",
        "drug_info": "Drug Information",
        "orig_ind": "Original indication",
        "ev_level": "Evidence level",
        "pred_ind_h": "Predicted indications ({m})",
        "full_report": "View full drug report →",
        "rel_news_h": "Related News ({n})",
        "unknown_date": "Unknown date",
        "source": "Source",
        "no_news": "*No related news yet. When news mentions this drug, it will be collected and shown here automatically.*",
        "disc_label": "Disclaimer",
        "disc_body": "The news on this page is collected automatically and is for research reference only; it does not constitute medical advice.",
        "desc_drug": "Health news related to {name}. Original indication: {ind}. {m} predicted indications.",
        "sum_ind": "<strong>{title}</strong> currently has <strong>{n} news articles</strong> and {m} related drugs.",
        "take_ind": "This page brings together the latest health news about “{kw}” and lists the drugs in the {proj} database whose predicted indications include this disease.",
        "rel_drugs": "Related drug reports",
        "rel_drugs_p": "The predicted indications of the following drugs may be related to this disease:",
        "desc_ind": "Health news about {title}. {n} articles, {m} related drugs.",
    },
    "zh": {
        "parent": "健康新聞",
        "title_news": "{name} 相關新聞",
        "back": "← 返回新聞總覽",
        "q": "{name} 有什麼相關新聞？",
        "sum_drug": "<strong>{name}</strong> 目前有 <strong>{n} 則</strong>相關新聞報導，預測適應症 {m} 個。",
        "take_drug": "本頁整合 {name} 的 AI 預測適應症與最新健康新聞，橘色標示的適應症表示近期有相關新聞報導。",
        "drug_info": "藥物資訊",
        "orig_ind": "原適應症",
        "ev_level": "證據等級",
        "pred_ind_h": "預測適應症（{m} 個）",
        "full_report": "查看完整藥物報告 →",
        "rel_news_h": "相關新聞（{n} 則）",
        "unknown_date": "未知日期",
        "source": "來源",
        "no_news": "*目前沒有相關新聞報導。當有新聞提到此藥物時，系統會自動收集並顯示在這裡。*",
        "disc_label": "免責聲明",
        "disc_body": "本頁新聞由系統自動收集，僅供研究參考，不構成醫療建議。",
        "desc_drug": "{name} 的相關健康新聞報導。原適應症：{ind}。預測適應症 {m} 個。",
        "sum_ind": "<strong>{title}</strong> 目前有 <strong>{n} 則</strong>相關新聞報導，{m} 個相關藥物。",
        "take_ind": "本頁整合「{kw}」相關的最新健康新聞，並列出 {proj} 資料庫中預測適應症包含此疾病的藥物。",
        "rel_drugs": "相關藥物報告",
        "rel_drugs_p": "以下藥物的預測適應症可能與此疾病相關：",
        "desc_ind": "{title} 的相關健康新聞報導。{n} 則新聞、{m} 個相關藥物。",
    },
    "es": {
        "parent": "Noticias de salud",
        "title_news": "Noticias sobre {name}",
        "back": "← Volver al resumen de noticias",
        "q": "¿Qué noticias hay sobre {name}?",
        "sum_drug": "<strong>{name}</strong> tiene actualmente <strong>{n} noticias</strong> y {m} indicaciones predichas.",
        "take_drug": "Esta página combina las indicaciones predichas por IA para {name} con las últimas noticias de salud. Las indicaciones resaltadas en naranja cuentan con cobertura informativa reciente.",
        "drug_info": "Información del medicamento",
        "orig_ind": "Indicación original",
        "ev_level": "Nivel de evidencia",
        "pred_ind_h": "Indicaciones predichas ({m})",
        "full_report": "Ver el informe completo del medicamento →",
        "rel_news_h": "Noticias relacionadas ({n})",
        "unknown_date": "Fecha desconocida",
        "source": "Fuente",
        "no_news": "*Todavía no hay noticias relacionadas. Cuando alguna noticia mencione este medicamento, se recopilará y se mostrará aquí automáticamente.*",
        "disc_label": "Descargo de responsabilidad",
        "disc_body": "Las noticias de esta página se recopilan automáticamente y son solo de referencia para investigación; no constituyen asesoramiento médico.",
        "desc_drug": "Noticias de salud relacionadas con {name}. Indicación original: {ind}. {m} indicaciones predichas.",
        "sum_ind": "<strong>{title}</strong> tiene actualmente <strong>{n} noticias</strong> y {m} medicamentos relacionados.",
        "take_ind": "Esta página reúne las últimas noticias de salud sobre «{kw}» y enumera los medicamentos de la base de datos {proj} cuyas indicaciones predichas incluyen esta enfermedad.",
        "rel_drugs": "Informes de medicamentos relacionados",
        "rel_drugs_p": "Las indicaciones predichas de los siguientes medicamentos pueden estar relacionadas con esta enfermedad:",
        "desc_ind": "Noticias de salud sobre {title}. {n} noticias, {m} medicamentos relacionados.",
    },
    "pt": {
        "parent": "Notícias de Saúde",
        "title_news": "Notícias sobre {name}",
        "back": "← Voltar à visão geral das notícias",
        "q": "Que notícias há sobre {name}?",
        "sum_drug": "<strong>{name}</strong> tem atualmente <strong>{n} notícias</strong> e {m} indicações previstas.",
        "take_drug": "Esta página combina as indicações previstas por IA para {name} com as notícias de saúde mais recentes. As indicações destacadas em laranja têm cobertura noticiosa recente.",
        "drug_info": "Informações do medicamento",
        "orig_ind": "Indicação original",
        "ev_level": "Nível de evidência",
        "pred_ind_h": "Indicações previstas ({m})",
        "full_report": "Ver o relatório completo do medicamento →",
        "rel_news_h": "Notícias relacionadas ({n})",
        "unknown_date": "Data desconhecida",
        "source": "Fonte",
        "no_news": "*Ainda não há notícias relacionadas. Quando uma notícia mencionar este medicamento, ela será recolhida e exibida aqui automaticamente.*",
        "disc_label": "Aviso de isenção de responsabilidade",
        "disc_body": "As notícias desta página são recolhidas automaticamente e servem apenas como referência para investigação; não constituem aconselhamento médico.",
        "desc_drug": "Notícias de saúde relacionadas com {name}. Indicação original: {ind}. {m} indicações previstas.",
        "sum_ind": "<strong>{title}</strong> tem atualmente <strong>{n} notícias</strong> e {m} medicamentos relacionados.",
        "take_ind": "Esta página reúne as notícias de saúde mais recentes sobre «{kw}» e lista os medicamentos da base de dados {proj} cujas indicações previstas incluem esta doença.",
        "rel_drugs": "Relatórios de medicamentos relacionados",
        "rel_drugs_p": "As indicações previstas dos seguintes medicamentos podem estar relacionadas com esta doença:",
        "desc_ind": "Notícias de saúde sobre {title}. {n} notícias, {m} medicamentos relacionados.",
    },
    "de": {
        "parent": "Gesundheitsnachrichten",
        "title_news": "Nachrichten zu {name}",
        "back": "← Zurück zur Nachrichtenübersicht",
        "q": "Welche Nachrichten gibt es zu {name}?",
        "sum_drug": "<strong>{name}</strong> hat derzeit <strong>{n} Nachrichtenbeiträge</strong> und {m} vorhergesagte Indikationen.",
        "take_drug": "Diese Seite verbindet die KI-vorhergesagten Indikationen für {name} mit den neuesten Gesundheitsnachrichten. Orange hervorgehobene Indikationen wurden kürzlich in den Nachrichten erwähnt.",
        "drug_info": "Arzneimittelinformationen",
        "orig_ind": "Ursprüngliche Indikation",
        "ev_level": "Evidenzniveau",
        "pred_ind_h": "Vorhergesagte Indikationen ({m})",
        "full_report": "Vollständigen Arzneimittelbericht ansehen →",
        "rel_news_h": "Verwandte Nachrichten ({n})",
        "unknown_date": "Unbekanntes Datum",
        "source": "Quelle",
        "no_news": "*Derzeit liegen keine verwandten Nachrichten vor. Sobald eine Meldung dieses Arzneimittel erwähnt, wird sie automatisch erfasst und hier angezeigt.*",
        "disc_label": "Haftungsausschluss",
        "disc_body": "Die Nachrichten auf dieser Seite werden automatisch gesammelt und dienen ausschließlich als Forschungsreferenz; sie stellen keine medizinische Beratung dar.",
        "desc_drug": "Gesundheitsnachrichten zu {name}. Ursprüngliche Indikation: {ind}. {m} vorhergesagte Indikationen.",
        "sum_ind": "<strong>{title}</strong> hat derzeit <strong>{n} Nachrichtenbeiträge</strong> und {m} verwandte Arzneimittel.",
        "take_ind": "Diese Seite bündelt die neuesten Gesundheitsnachrichten zu „{kw}“ und listet die Arzneimittel aus der {proj}-Datenbank auf, deren vorhergesagte Indikationen diese Krankheit umfassen.",
        "rel_drugs": "Verwandte Arzneimittelberichte",
        "rel_drugs_p": "Die vorhergesagten Indikationen der folgenden Arzneimittel könnten mit dieser Krankheit zusammenhängen:",
        "desc_ind": "Gesundheitsnachrichten zu {title}. {n} Beiträge, {m} verwandte Arzneimittel.",
    },
    "da": {
        "parent": "Sundhedsnyheder",
        "title_news": "Nyheder om {name}",
        "back": "← Tilbage til nyhedsoversigten",
        "q": "Hvilke nyheder er der om {name}?",
        "sum_drug": "<strong>{name}</strong> har i øjeblikket <strong>{n} nyhedsartikler</strong> og {m} forudsagte indikationer.",
        "take_drug": "Denne side kombinerer de AI-forudsagte indikationer for {name} med de seneste sundhedsnyheder. Indikationer markeret med orange har været omtalt i nyhederne for nylig.",
        "drug_info": "Lægemiddeloplysninger",
        "orig_ind": "Oprindelig indikation",
        "ev_level": "Evidensniveau",
        "pred_ind_h": "Forudsagte indikationer ({m})",
        "full_report": "Se den fulde lægemiddelrapport →",
        "rel_news_h": "Relaterede nyheder ({n})",
        "unknown_date": "Ukendt dato",
        "source": "Kilde",
        "no_news": "*Der er endnu ingen relaterede nyheder. Når en nyhed nævner dette lægemiddel, bliver den automatisk indsamlet og vist her.*",
        "disc_label": "Ansvarsfraskrivelse",
        "disc_body": "Nyhederne på denne side indsamles automatisk og er kun til forskningsbrug; de udgør ikke medicinsk rådgivning.",
        "desc_drug": "Sundhedsnyheder om {name}. Oprindelig indikation: {ind}. {m} forudsagte indikationer.",
        "sum_ind": "<strong>{title}</strong> har i øjeblikket <strong>{n} nyhedsartikler</strong> og {m} relaterede lægemidler.",
        "take_ind": "Denne side samler de seneste sundhedsnyheder om “{kw}” og viser de lægemidler i {proj}-databasen, hvis forudsagte indikationer omfatter denne sygdom.",
        "rel_drugs": "Relaterede lægemiddelrapporter",
        "rel_drugs_p": "De forudsagte indikationer for følgende lægemidler kan være relateret til denne sygdom:",
        "desc_ind": "Sundhedsnyheder om {title}. {n} artikler, {m} relaterede lægemidler.",
    },
    "fi": {
        "parent": "Terveysuutiset",
        "title_news": "{name} – uutiset",
        "back": "← Takaisin uutiskatsaukseen",
        "q": "Mitä uutisia lääkkeestä {name} on?",
        "sum_drug": "Lääkkeestä <strong>{name}</strong> on tällä hetkellä <strong>{n} uutista</strong> ja {m} ennustettua käyttöaihetta.",
        "take_drug": "Tämä sivu yhdistää lääkkeen {name} tekoälyn ennustamat käyttöaiheet tuoreimpiin terveysuutisiin. Oranssilla korostetuista käyttöaiheista on hiljattain uutisoitu.",
        "drug_info": "Lääketiedot",
        "orig_ind": "Alkuperäinen käyttöaihe",
        "ev_level": "Näytön taso",
        "pred_ind_h": "Ennustetut käyttöaiheet ({m})",
        "full_report": "Katso koko lääkeraportti →",
        "rel_news_h": "Aiheeseen liittyvät uutiset ({n})",
        "unknown_date": "Tuntematon päivämäärä",
        "source": "Lähde",
        "no_news": "*Aiheeseen liittyviä uutisia ei vielä ole. Kun uutisessa mainitaan tämä lääke, se kerätään ja näytetään tässä automaattisesti.*",
        "disc_label": "Vastuuvapauslauseke",
        "disc_body": "Tämän sivun uutiset kerätään automaattisesti ja ne on tarkoitettu vain tutkimuskäyttöön; ne eivät ole lääketieteellistä neuvontaa.",
        "desc_drug": "Lääkkeeseen {name} liittyvät terveysuutiset. Alkuperäinen käyttöaihe: {ind}. {m} ennustettua käyttöaihetta.",
        "sum_ind": "Aiheesta <strong>{title}</strong> on tällä hetkellä <strong>{n} uutista</strong> ja {m} siihen liittyvää lääkettä.",
        "take_ind": "Tämä sivu kokoaa tuoreimmat terveysuutiset aiheesta ”{kw}” ja listaa {proj}-tietokannan lääkkeet, joiden ennustettuihin käyttöaiheisiin tämä sairaus kuuluu.",
        "rel_drugs": "Aiheeseen liittyvät lääkeraportit",
        "rel_drugs_p": "Seuraavien lääkkeiden ennustetut käyttöaiheet voivat liittyä tähän sairauteen:",
        "desc_ind": "Terveysuutiset aiheesta {title}. {n} uutista, {m} liittyvää lääkettä.",
    },
    "fr": {
        "parent": "Actualités santé",
        "title_news": "Actualités sur {name}",
        "back": "← Retour à l’aperçu des actualités",
        "q": "Quelles actualités concernent {name} ?",
        "sum_drug": "<strong>{name}</strong> compte actuellement <strong>{n} articles d’actualité</strong> et {m} indications prédites.",
        "take_drug": "Cette page associe les indications prédites par l’IA pour {name} aux dernières actualités santé. Les indications surlignées en orange ont fait l’objet d’une couverture médiatique récente.",
        "drug_info": "Informations sur le médicament",
        "orig_ind": "Indication initiale",
        "ev_level": "Niveau de preuve",
        "pred_ind_h": "Indications prédites ({m})",
        "full_report": "Voir le rapport complet du médicament →",
        "rel_news_h": "Actualités associées ({n})",
        "unknown_date": "Date inconnue",
        "source": "Source",
        "no_news": "*Aucune actualité associée pour le moment. Dès qu’un article mentionnera ce médicament, il sera collecté et affiché ici automatiquement.*",
        "disc_label": "Avertissement",
        "disc_body": "Les actualités de cette page sont collectées automatiquement et servent uniquement de référence pour la recherche ; elles ne constituent pas un avis médical.",
        "desc_drug": "Actualités santé concernant {name}. Indication initiale : {ind}. {m} indications prédites.",
        "sum_ind": "<strong>{title}</strong> compte actuellement <strong>{n} articles d’actualité</strong> et {m} médicaments associés.",
        "take_ind": "Cette page rassemble les dernières actualités santé sur «&nbsp;{kw}&nbsp;» et répertorie les médicaments de la base {proj} dont les indications prédites incluent cette maladie.",
        "rel_drugs": "Rapports de médicaments associés",
        "rel_drugs_p": "Les indications prédites des médicaments suivants pourraient être liées à cette maladie :",
        "desc_ind": "Actualités santé sur {title}. {n} articles, {m} médicaments associés.",
    },
    "it": {
        "parent": "Notizie sulla salute",
        "title_news": "Notizie su {name}",
        "back": "← Torna alla panoramica delle notizie",
        "q": "Quali notizie riguardano {name}?",
        "sum_drug": "<strong>{name}</strong> conta attualmente <strong>{n} notizie</strong> e {m} indicazioni previste.",
        "take_drug": "Questa pagina combina le indicazioni previste dall’IA per {name} con le ultime notizie sulla salute. Le indicazioni evidenziate in arancione sono state oggetto di notizie recenti.",
        "drug_info": "Informazioni sul farmaco",
        "orig_ind": "Indicazione originale",
        "ev_level": "Livello di evidenza",
        "pred_ind_h": "Indicazioni previste ({m})",
        "full_report": "Vedi il rapporto completo sul farmaco →",
        "rel_news_h": "Notizie correlate ({n})",
        "unknown_date": "Data sconosciuta",
        "source": "Fonte",
        "no_news": "*Al momento non ci sono notizie correlate. Quando una notizia menzionerà questo farmaco, verrà raccolta e mostrata qui automaticamente.*",
        "disc_label": "Avvertenza",
        "disc_body": "Le notizie di questa pagina sono raccolte automaticamente e hanno solo valore di riferimento per la ricerca; non costituiscono un parere medico.",
        "desc_drug": "Notizie sulla salute relative a {name}. Indicazione originale: {ind}. {m} indicazioni previste.",
        "sum_ind": "<strong>{title}</strong> conta attualmente <strong>{n} notizie</strong> e {m} farmaci correlati.",
        "take_ind": "Questa pagina raccoglie le ultime notizie sulla salute riguardanti «{kw}» ed elenca i farmaci della banca dati {proj} le cui indicazioni previste includono questa malattia.",
        "rel_drugs": "Rapporti sui farmaci correlati",
        "rel_drugs_p": "Le indicazioni previste dei seguenti farmaci potrebbero essere correlate a questa malattia:",
        "desc_ind": "Notizie sulla salute su {title}. {n} notizie, {m} farmaci correlati.",
    },
    "ja": {
        "parent": "健康ニュース",
        "title_news": "{name} 関連ニュース",
        "back": "← ニュース一覧に戻る",
        "q": "{name} に関するニュースは？",
        "sum_drug": "<strong>{name}</strong> には現在 <strong>{n} 件</strong>の関連ニュースがあり、予測適応症は {m} 件です。",
        "take_drug": "このページは {name} のAI予測適応症と最新の健康ニュースをまとめたものです。オレンジ色で示された適応症は、最近ニュースで取り上げられたことを示します。",
        "drug_info": "医薬品情報",
        "orig_ind": "既存適応症",
        "ev_level": "エビデンスレベル",
        "pred_ind_h": "予測適応症（{m} 件）",
        "full_report": "医薬品レポート全文を見る →",
        "rel_news_h": "関連ニュース（{n} 件）",
        "unknown_date": "日付不明",
        "source": "出典",
        "no_news": "*現在、関連ニュースはありません。この医薬品に言及するニュースが出ると、自動的に収集されここに表示されます。*",
        "disc_label": "免責事項",
        "disc_body": "本ページのニュースはシステムが自動収集したものであり、研究上の参考情報にすぎず、医療アドバイスを構成するものではありません。",
        "desc_drug": "{name} に関する健康ニュース。既存適応症：{ind}。予測適応症 {m} 件。",
        "sum_ind": "<strong>{title}</strong> には現在 <strong>{n} 件</strong>の関連ニュースと {m} 件の関連医薬品があります。",
        "take_ind": "このページは「{kw}」に関する最新の健康ニュースをまとめ、{proj} データベースで予測適応症にこの疾患を含む医薬品を一覧表示します。",
        "rel_drugs": "関連医薬品レポート",
        "rel_drugs_p": "以下の医薬品の予測適応症は、この疾患と関連している可能性があります：",
        "desc_ind": "{title} に関する健康ニュース。ニュース {n} 件、関連医薬品 {m} 件。",
    },
    "ko": {
        "parent": "건강 뉴스",
        "title_news": "{name} 관련 뉴스",
        "back": "← 뉴스 전체 보기로 돌아가기",
        "q": "{name} 관련 뉴스는 무엇인가요?",
        "sum_drug": "<strong>{name}</strong> 관련 뉴스는 현재 <strong>{n}건</strong>이며, 예측 적응증은 {m}개입니다.",
        "take_drug": "이 페이지는 {name}의 AI 예측 적응증과 최신 건강 뉴스를 함께 보여줍니다. 주황색으로 표시된 적응증은 최근 뉴스에 보도된 것입니다.",
        "drug_info": "의약품 정보",
        "orig_ind": "기존 적응증",
        "ev_level": "근거 수준",
        "pred_ind_h": "예측 적응증 ({m}개)",
        "full_report": "전체 의약품 보고서 보기 →",
        "rel_news_h": "관련 뉴스 ({n}건)",
        "unknown_date": "날짜 미상",
        "source": "출처",
        "no_news": "*현재 관련 뉴스가 없습니다. 이 의약품을 언급한 뉴스가 나오면 자동으로 수집되어 여기에 표시됩니다.*",
        "disc_label": "면책 조항",
        "disc_body": "이 페이지의 뉴스는 시스템이 자동으로 수집한 것으로 연구 참고용일 뿐이며 의학적 조언을 구성하지 않습니다.",
        "desc_drug": "{name} 관련 건강 뉴스. 기존 적응증: {ind}. 예측 적응증 {m}개.",
        "sum_ind": "<strong>{title}</strong> 관련 뉴스는 현재 <strong>{n}건</strong>이며, 관련 의약품은 {m}개입니다.",
        "take_ind": "이 페이지는 ‘{kw}’ 관련 최신 건강 뉴스를 모으고, {proj} 데이터베이스에서 예측 적응증에 이 질환이 포함된 의약품을 보여줍니다.",
        "rel_drugs": "관련 의약품 보고서",
        "rel_drugs_p": "다음 의약품의 예측 적응증이 이 질환과 관련 있을 수 있습니다:",
        "desc_ind": "{title} 관련 건강 뉴스. 뉴스 {n}건, 관련 의약품 {m}개.",
    },
    "ms": {
        "parent": "Berita Kesihatan",
        "title_news": "Berita berkaitan {name}",
        "back": "← Kembali ke ringkasan berita",
        "q": "Apakah berita berkaitan {name}?",
        "sum_drug": "<strong>{name}</strong> kini mempunyai <strong>{n} berita</strong> dan {m} indikasi diramal.",
        "take_drug": "Halaman ini menggabungkan indikasi ramalan AI bagi {name} dengan berita kesihatan terkini. Indikasi yang ditandakan oren mempunyai liputan berita terbaharu.",
        "drug_info": "Maklumat ubat",
        "orig_ind": "Indikasi asal",
        "ev_level": "Tahap bukti",
        "pred_ind_h": "Indikasi diramal ({m})",
        "full_report": "Lihat laporan penuh ubat →",
        "rel_news_h": "Berita berkaitan ({n})",
        "unknown_date": "Tarikh tidak diketahui",
        "source": "Sumber",
        "no_news": "*Tiada berita berkaitan buat masa ini. Apabila ada berita menyebut ubat ini, ia akan dikumpulkan dan dipaparkan di sini secara automatik.*",
        "disc_label": "Penafian",
        "disc_body": "Berita di halaman ini dikumpulkan secara automatik dan hanya sebagai rujukan penyelidikan; ia bukan nasihat perubatan.",
        "desc_drug": "Berita kesihatan berkaitan {name}. Indikasi asal: {ind}. {m} indikasi diramal.",
        "sum_ind": "<strong>{title}</strong> kini mempunyai <strong>{n} berita</strong> dan {m} ubat berkaitan.",
        "take_ind": "Halaman ini menghimpunkan berita kesihatan terkini tentang “{kw}” dan menyenaraikan ubat dalam pangkalan data {proj} yang indikasi ramalannya merangkumi penyakit ini.",
        "rel_drugs": "Laporan ubat berkaitan",
        "rel_drugs_p": "Indikasi ramalan bagi ubat berikut mungkin berkaitan dengan penyakit ini:",
        "desc_ind": "Berita kesihatan tentang {title}. {n} berita, {m} ubat berkaitan.",
    },
    "nl": {
        "parent": "Gezondheidsnieuws",
        "title_news": "Nieuws over {name}",
        "back": "← Terug naar nieuwsoverzicht",
        "q": "Welk nieuws is er over {name}?",
        "sum_drug": "<strong>{name}</strong> heeft momenteel <strong>{n} nieuwsberichten</strong> en {m} voorspelde indicaties.",
        "take_drug": "Deze pagina combineert de door AI voorspelde indicaties voor {name} met het laatste gezondheidsnieuws. Oranje gemarkeerde indicaties zijn recent in het nieuws geweest.",
        "drug_info": "Geneesmiddelinformatie",
        "orig_ind": "Oorspronkelijke indicatie",
        "ev_level": "Bewijsniveau",
        "pred_ind_h": "Voorspelde indicaties ({m})",
        "full_report": "Bekijk het volledige geneesmiddelrapport →",
        "rel_news_h": "Gerelateerd nieuws ({n})",
        "unknown_date": "Onbekende datum",
        "source": "Bron",
        "no_news": "*Er is nog geen gerelateerd nieuws. Zodra een bericht dit geneesmiddel noemt, wordt het automatisch verzameld en hier getoond.*",
        "disc_label": "Disclaimer",
        "disc_body": "Het nieuws op deze pagina wordt automatisch verzameld en dient uitsluitend als onderzoeksreferentie; het vormt geen medisch advies.",
        "desc_drug": "Gezondheidsnieuws over {name}. Oorspronkelijke indicatie: {ind}. {m} voorspelde indicaties.",
        "sum_ind": "<strong>{title}</strong> heeft momenteel <strong>{n} nieuwsberichten</strong> en {m} gerelateerde geneesmiddelen.",
        "take_ind": "Deze pagina bundelt het laatste gezondheidsnieuws over “{kw}” en toont de geneesmiddelen in de {proj}-database waarvan de voorspelde indicaties deze ziekte omvatten.",
        "rel_drugs": "Gerelateerde geneesmiddelrapporten",
        "rel_drugs_p": "De voorspelde indicaties van de volgende geneesmiddelen kunnen met deze ziekte samenhangen:",
        "desc_ind": "Gezondheidsnieuws over {title}. {n} berichten, {m} gerelateerde geneesmiddelen.",
    },
    "no": {
        "parent": "Helsenyheter",
        "title_news": "Nyheter om {name}",
        "back": "← Tilbake til nyhetsoversikten",
        "q": "Hvilke nyheter finnes om {name}?",
        "sum_drug": "<strong>{name}</strong> har for tiden <strong>{n} nyhetssaker</strong> og {m} predikerte indikasjoner.",
        "take_drug": "Denne siden kombinerer de AI-predikerte indikasjonene for {name} med de siste helsenyhetene. Indikasjoner merket med oransje har vært omtalt i nyhetene nylig.",
        "drug_info": "Legemiddelinformasjon",
        "orig_ind": "Opprinnelig indikasjon",
        "ev_level": "Evidensnivå",
        "pred_ind_h": "Predikerte indikasjoner ({m})",
        "full_report": "Se hele legemiddelrapporten →",
        "rel_news_h": "Relaterte nyheter ({n})",
        "unknown_date": "Ukjent dato",
        "source": "Kilde",
        "no_news": "*Det finnes ingen relaterte nyheter ennå. Når en nyhet nevner dette legemidlet, blir den automatisk samlet inn og vist her.*",
        "disc_label": "Ansvarsfraskrivelse",
        "disc_body": "Nyhetene på denne siden samles inn automatisk og er kun ment som forskningsreferanse; de utgjør ikke medisinsk rådgivning.",
        "desc_drug": "Helsenyheter om {name}. Opprinnelig indikasjon: {ind}. {m} predikerte indikasjoner.",
        "sum_ind": "<strong>{title}</strong> har for tiden <strong>{n} nyhetssaker</strong> og {m} relaterte legemidler.",
        "take_ind": "Denne siden samler de siste helsenyhetene om «{kw}» og viser legemidlene i {proj}-databasen der de predikerte indikasjonene omfatter denne sykdommen.",
        "rel_drugs": "Relaterte legemiddelrapporter",
        "rel_drugs_p": "De predikerte indikasjonene for følgende legemidler kan være relatert til denne sykdommen:",
        "desc_ind": "Helsenyheter om {title}. {n} saker, {m} relaterte legemidler.",
    },
    "sv": {
        "parent": "Hälsonyheter",
        "title_news": "Nyheter om {name}",
        "back": "← Tillbaka till nyhetsöversikten",
        "q": "Vilka nyheter finns om {name}?",
        "sum_drug": "<strong>{name}</strong> har för närvarande <strong>{n} nyhetsartiklar</strong> och {m} förutsagda indikationer.",
        "take_drug": "Den här sidan kombinerar de AI-förutsagda indikationerna för {name} med de senaste hälsonyheterna. Indikationer markerade i orange har uppmärksammats i nyheterna nyligen.",
        "drug_info": "Läkemedelsinformation",
        "orig_ind": "Ursprunglig indikation",
        "ev_level": "Evidensnivå",
        "pred_ind_h": "Förutsagda indikationer ({m})",
        "full_report": "Se hela läkemedelsrapporten →",
        "rel_news_h": "Relaterade nyheter ({n})",
        "unknown_date": "Okänt datum",
        "source": "Källa",
        "no_news": "*Det finns inga relaterade nyheter ännu. När en nyhet nämner detta läkemedel samlas den in och visas här automatiskt.*",
        "disc_label": "Ansvarsfriskrivning",
        "disc_body": "Nyheterna på den här sidan samlas in automatiskt och är endast avsedda som forskningsreferens; de utgör inte medicinsk rådgivning.",
        "desc_drug": "Hälsonyheter om {name}. Ursprunglig indikation: {ind}. {m} förutsagda indikationer.",
        "sum_ind": "<strong>{title}</strong> har för närvarande <strong>{n} nyhetsartiklar</strong> och {m} relaterade läkemedel.",
        "take_ind": "Den här sidan samlar de senaste hälsonyheterna om ”{kw}” och listar de läkemedel i {proj}-databasen vars förutsagda indikationer omfattar denna sjukdom.",
        "rel_drugs": "Relaterade läkemedelsrapporter",
        "rel_drugs_p": "De förutsagda indikationerna för följande läkemedel kan vara relaterade till denna sjukdom:",
        "desc_ind": "Hälsonyheter om {title}. {n} artiklar, {m} relaterade läkemedel.",
    },
    "ar": {
        "parent": "أخبار صحية",
        "title_news": "أخبار عن {name}",
        "back": "← العودة إلى نظرة عامة على الأخبار",
        "q": "ما الأخبار المتعلقة بـ {name}؟",
        "sum_drug": "يوجد حاليًا <strong>{n} خبرًا</strong> عن <strong>{name}</strong>، مع {m} من دواعي الاستعمال المتوقعة.",
        "take_drug": "تجمع هذه الصفحة بين دواعي الاستعمال التي تنبأ بها الذكاء الاصطناعي لـ {name} وأحدث الأخبار الصحية. الدواعي المميزة باللون البرتقالي وردت في أخبار حديثة.",
        "drug_info": "معلومات الدواء",
        "orig_ind": "دواعي الاستعمال الأصلية",
        "ev_level": "مستوى الأدلة",
        "pred_ind_h": "دواعي الاستعمال المتوقعة ({m})",
        "full_report": "عرض تقرير الدواء الكامل ←",
        "rel_news_h": "أخبار ذات صلة ({n})",
        "unknown_date": "تاريخ غير معروف",
        "source": "المصدر",
        "no_news": "*لا توجد أخبار ذات صلة حتى الآن. عندما يرد ذكر هذا الدواء في الأخبار، سيتم جمعه وعرضه هنا تلقائيًا.*",
        "disc_label": "إخلاء المسؤولية",
        "disc_body": "تُجمع أخبار هذه الصفحة تلقائيًا وهي للاطلاع البحثي فقط ولا تشكل نصيحة طبية.",
        "desc_drug": "أخبار صحية متعلقة بـ {name}. دواعي الاستعمال الأصلية: {ind}. {m} من دواعي الاستعمال المتوقعة.",
        "sum_ind": "يوجد حاليًا <strong>{n} خبرًا</strong> عن <strong>{title}</strong> و{m} من الأدوية ذات الصلة.",
        "take_ind": "تجمع هذه الصفحة أحدث الأخبار الصحية عن «{kw}» وتعرض أدوية قاعدة بيانات {proj} التي تشمل دواعي استعمالها المتوقعة هذا المرض.",
        "rel_drugs": "تقارير الأدوية ذات الصلة",
        "rel_drugs_p": "قد تكون دواعي الاستعمال المتوقعة للأدوية التالية ذات صلة بهذا المرض:",
        "desc_ind": "أخبار صحية عن {title}. {n} خبرًا، {m} من الأدوية ذات الصلة.",
    },
    "th": {
        "parent": "ข่าวสุขภาพ",
        "title_news": "ข่าวเกี่ยวกับ {name}",
        "back": "← กลับไปที่ภาพรวมข่าว",
        "q": "มีข่าวอะไรเกี่ยวกับ {name} บ้าง",
        "sum_drug": "ขณะนี้ <strong>{name}</strong> มีข่าวที่เกี่ยวข้อง <strong>{n} ข่าว</strong> และข้อบ่งใช้ที่คาดการณ์ {m} รายการ",
        "take_drug": "หน้านี้รวมข้อบ่งใช้ที่คาดการณ์โดย AI ของ {name} เข้ากับข่าวสุขภาพล่าสุด ข้อบ่งใช้ที่เน้นสีส้มคือรายการที่มีข่าวรายงานเมื่อเร็ว ๆ นี้",
        "drug_info": "ข้อมูลยา",
        "orig_ind": "ข้อบ่งใช้เดิม",
        "ev_level": "ระดับหลักฐาน",
        "pred_ind_h": "ข้อบ่งใช้ที่คาดการณ์ ({m} รายการ)",
        "full_report": "ดูรายงานยาฉบับเต็ม →",
        "rel_news_h": "ข่าวที่เกี่ยวข้อง ({n} ข่าว)",
        "unknown_date": "ไม่ทราบวันที่",
        "source": "แหล่งที่มา",
        "no_news": "*ยังไม่มีข่าวที่เกี่ยวข้อง เมื่อมีข่าวกล่าวถึงยานี้ ระบบจะรวบรวมและแสดงที่นี่โดยอัตโนมัติ*",
        "disc_label": "ข้อจำกัดความรับผิดชอบ",
        "disc_body": "ข่าวในหน้านี้รวบรวมโดยระบบอัตโนมัติ ใช้เพื่อการอ้างอิงเชิงวิจัยเท่านั้น และไม่ถือเป็นคำแนะนำทางการแพทย์",
        "desc_drug": "ข่าวสุขภาพที่เกี่ยวข้องกับ {name} ข้อบ่งใช้เดิม: {ind} ข้อบ่งใช้ที่คาดการณ์ {m} รายการ",
        "sum_ind": "ขณะนี้ <strong>{title}</strong> มีข่าวที่เกี่ยวข้อง <strong>{n} ข่าว</strong> และยาที่เกี่ยวข้อง {m} รายการ",
        "take_ind": "หน้านี้รวบรวมข่าวสุขภาพล่าสุดเกี่ยวกับ “{kw}” และแสดงรายการยาในฐานข้อมูล {proj} ที่มีโรคนี้อยู่ในข้อบ่งใช้ที่คาดการณ์",
        "rel_drugs": "รายงานยาที่เกี่ยวข้อง",
        "rel_drugs_p": "ข้อบ่งใช้ที่คาดการณ์ของยาต่อไปนี้อาจเกี่ยวข้องกับโรคนี้:",
        "desc_ind": "ข่าวสุขภาพเกี่ยวกับ {title} ข่าว {n} รายการ ยาที่เกี่ยวข้อง {m} รายการ",
    },
}

PROJECT_NAME = PROJECT_ROOT.name
LANG = LANG_BY_PROJECT.get(PROJECT_NAME, "en")
N = NEWS_STRINGS.get(LANG, NEWS_STRINGS["en"])


def _news_parent() -> str:
    """新聞頁的 Jekyll 母頁標題：以站台自己的 docs/news.md 為準，沒有才用字串表。"""
    nav = DOCS_DIR / "news.md"
    if nav.exists():
        import re as _re
        m = _re.search(r"^title:\s*(.+?)\s*$", nav.read_text(encoding="utf-8"), _re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return N["parent"]


NEWS_PARENT = _news_parent()


def load_json(path: Path) -> dict | list:
    """載入 JSON 檔案"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict | list, path: Path):
    """儲存 JSON 檔案"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_all_sources() -> list[dict]:
    """載入所有來源的新聞"""
    all_news = []
    excluded = {"keywords.json", "matched_news.json"}

    for json_file in DATA_DIR.glob("*.json"):
        if json_file.name in excluded:
            continue

        try:
            data = load_json(json_file)
            source_name = data.get("source", json_file.stem)
            news_items = data.get("news", [])
            print(f"  - {json_file.name}: {len(news_items)} 則")

            for item in news_items:
                item["_source_file"] = source_name
                all_news.append(item)

        except Exception as e:
            print(f"  警告: 無法載入 {json_file.name} - {e}")

    return all_news


def filter_old_news(news_items: list[dict]) -> list[dict]:
    """過濾超過 30 天的舊新聞"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_NEWS_AGE_DAYS)
    filtered = []

    for item in news_items:
        try:
            published = datetime.fromisoformat(item.get("published", ""))
            if published >= cutoff:
                filtered.append(item)
        except (ValueError, TypeError):
            # 無法解析日期，保留
            filtered.append(item)

    removed = len(news_items) - len(filtered)
    if removed > 0:
        print(f"  過濾舊新聞: {removed} 則")

    return filtered


def title_similarity(title1: str, title2: str) -> float:
    """計算兩個標題的相似度"""
    # 移除來源標記（如「- 聯合報」）
    clean1 = re.sub(r"\s*[-–—]\s*[^\s]+$", "", title1).strip()
    clean2 = re.sub(r"\s*[-–—]\s*[^\s]+$", "", title2).strip()

    return SequenceMatcher(None, clean1, clean2).ratio()


def deduplicate_news(news_items: list[dict]) -> list[dict]:
    """跨站去重，合併相似新聞的來源"""
    # 按發布時間排序（最新的在前）
    sorted_news = sorted(
        news_items,
        key=lambda x: x.get("published", ""),
        reverse=True
    )

    merged = []
    used_indices = set()

    for i, item in enumerate(sorted_news):
        if i in used_indices:
            continue

        # 找出相似的新聞
        similar_items = [item]
        item_time = datetime.fromisoformat(
            item.get("published", datetime.now(timezone.utc).isoformat())
        )

        for j, other in enumerate(sorted_news[i + 1:], start=i + 1):
            if j in used_indices:
                continue

            # 檢查時間窗口
            other_time = datetime.fromisoformat(
                other.get("published", datetime.now(timezone.utc).isoformat())
            )
            time_diff = abs((item_time - other_time).total_seconds() / 3600)

            if time_diff > TIME_WINDOW_HOURS:
                continue

            # 檢查標題相似度
            if title_similarity(item["title"], other["title"]) >= SIMILARITY_THRESHOLD:
                similar_items.append(other)
                used_indices.add(j)

        # 合併來源
        all_sources = []
        seen_links = set()
        for sim_item in similar_items:
            for source in sim_item.get("sources", []):
                if source["link"] not in seen_links:
                    seen_links.add(source["link"])
                    all_sources.append(source)

        # 使用最早的發布時間
        earliest_time = min(
            datetime.fromisoformat(s.get("published", datetime.now(timezone.utc).isoformat()))
            for s in similar_items
        )

        merged_item = {
            "id": item["id"],
            "title": re.sub(r"\s*[-–—]\s*[^\s]+$", "", item["title"]).strip(),
            "published": earliest_time.isoformat(),
            "summary": item.get("summary", ""),
            "sources": all_sources,
            "matched_keywords": []  # 稍後填入
        }
        merged.append(merged_item)
        used_indices.add(i)

    print(f"  去重後: {len(merged)} 則（合併 {len(news_items) - len(merged)} 則）")
    return merged


def match_keywords(news_items: list[dict], keywords: dict) -> list[dict]:
    """對新聞進行關鍵字匹配"""
    drugs = keywords.get("drugs", [])
    indications = keywords.get("indications", [])

    # 建立藥物 slug -> name 的對照表
    drug_name_map = {d["slug"]: d["name"] for d in drugs}

    matched_count = 0

    for item in news_items:
        text_to_search = f"{item['title']} {item.get('summary', '')}".lower()
        matches = []

        # 匹配藥物
        for drug in drugs:
            drug_name = drug["name"]
            drug_slug = drug["slug"]

            # 處理 keywords 可能是 list 或 dict 的情況
            drug_keywords = drug.get("keywords", [])
            if isinstance(drug_keywords, dict):
                en_keywords = drug_keywords.get("en", [])
            else:
                en_keywords = drug_keywords if isinstance(drug_keywords, list) else []

            # 英文關鍵字
            for kw in en_keywords:
                if kw.lower() in text_to_search:
                    matches.append({
                        "type": "drug",
                        "slug": drug_slug,
                        "keyword": kw,
                        "name": drug_name,
                        "url": drug["url"]
                    })
                    break  # 同一藥物只記錄一次

            # 中文關鍵字
            zh_keywords = drug_keywords.get("zh", []) if isinstance(drug_keywords, dict) else []
            for kw in zh_keywords:
                if kw in item["title"] or kw in item.get("summary", ""):
                    # 確保沒有重複
                    if not any(m["slug"] == drug_slug for m in matches):
                        matches.append({
                            "type": "drug",
                            "slug": drug_slug,
                            "keyword": kw,
                            "name": drug_name,
                            "url": drug["url"]
                        })
                    break

        # 匹配適應症
        for ind in indications:
            ind_name = ind["name"]

            # 將 related_drugs 從 slug 轉換為 {slug, name} 格式
            related_drugs = [
                {"slug": slug, "name": drug_name_map.get(slug, slug)}
                for slug in ind.get("related_drugs", [])
            ]

            # 處理 indication keywords 可能是 list 或 dict 的情況
            ind_keywords = ind.get("keywords", [])
            if isinstance(ind_keywords, dict):
                ind_en_keywords = ind_keywords.get("en", [])
                ind_zh_keywords = ind_keywords.get("zh", [])
            else:
                ind_en_keywords = ind_keywords if isinstance(ind_keywords, list) else []
                ind_zh_keywords = []

            # 英文關鍵字
            for kw in ind_en_keywords:
                if kw.lower() in text_to_search:
                    matches.append({
                        "type": "indication",
                        "name": ind_name,
                        "keyword": kw,
                        "related_drugs": related_drugs
                    })
                    break

            # 中文關鍵字
            for kw in ind_zh_keywords:
                if kw in item["title"] or kw in item.get("summary", ""):
                    # 確保同一關鍵字沒有重複（避免 "感冒" 同時出現在 "common cold" 和 "感冒" 兩個條目）
                    if not any(m.get("keyword") == kw and m["type"] == "indication" for m in matches):
                        matches.append({
                            "type": "indication",
                            "name": ind_name,
                            "keyword": kw,
                            "related_drugs": related_drugs
                        })
                    break

        # keywords.json 只包含有相關藥物的關鍵字，無需再過濾
        item["matched_keywords"] = matches
        if matches:
            matched_count += 1

    print(f"  匹配到關鍵字: {matched_count} 則")
    return news_items


def generate_news_pages(matched_news: list[dict], keywords: dict):
    """產生 Jekyll 新聞頁面"""
    # 確保目錄存在
    NEWS_COLLECTION_DIR.mkdir(parents=True, exist_ok=True)

    # 清除舊頁面
    for old_file in NEWS_COLLECTION_DIR.glob("*.md"):
        old_file.unlink()

    # 載入完整的藥物資料（包含 original_indication 等）
    drugs_data_path = DOCS_DIR / "data" / "drugs.json"
    drugs_data = load_json(drugs_data_path) if drugs_data_path.exists() else {"drugs": []}
    # 各站 drugs.json 的 key 不一致（有的用 slug，有的用 drugbank_id），兩種都接受
    drugs_detail_map = {}
    for d in drugs_data.get("drugs", []):
        key = d.get("slug") or d.get("drugbank_id")
        if key:
            drugs_detail_map[str(key).lower()] = d

    # 載入搜尋索引（包含完整的預測適應症列表）
    search_index_path = DOCS_DIR / "data" / "search-index.json"
    search_index = load_json(search_index_path) if search_index_path.exists() else {"drugs": []}
    search_index_map = {d["slug"]: d for d in search_index.get("drugs", [])}

    # 建立藥物和適應症的新聞索引
    drug_news = {}  # slug -> [news_items]
    indication_news = {}  # name -> [news_items]

    for item in matched_news:
        if not item.get("matched_keywords"):
            continue

        for match in item["matched_keywords"]:
            if match["type"] == "drug":
                slug = match["slug"]
                if slug not in drug_news:
                    drug_news[slug] = []
                drug_news[slug].append(item)
            elif match["type"] == "indication":
                name = match["name"]
                if name not in indication_news:
                    indication_news[name] = []
                indication_news[name].append(item)
                # 也把新聞加到相關藥物
                for related_drug in match.get("related_drugs", []):
                    slug = related_drug.get("slug")
                    if slug:
                        if slug not in drug_news:
                            drug_news[slug] = []
                        # 避免重複加入同一則新聞
                        if item not in drug_news[slug]:
                            drug_news[slug].append(item)

    # 產生所有藥物新聞頁面（191 個全部生成）
    drugs_map = {d["slug"]: d for d in keywords.get("drugs", [])}
    drug_count = 0

    for drug in keywords.get("drugs", []):
        slug = drug["slug"]
        drug_info = drugs_map.get(slug, {})
        drug_detail = drugs_detail_map.get(str(slug).lower(), {})
        drug_search = search_index_map.get(slug, {})
        news_items = drug_news.get(slug, [])  # 可能為空
        generate_drug_news_page(slug, drug_info, drug_detail, drug_search, news_items)
        drug_count += 1

    # 產生適應症新聞頁面（只有匹配到新聞的）
    for name, items in indication_news.items():
        generate_indication_news_page(name, items, keywords)

    print(f"  產生頁面: {drug_count} 藥物 + {len(indication_news)} 適應症")


def slugify(text: str) -> str:
    """將文字轉換為 URL-safe 的 slug"""
    # 移除特殊字符，保留英文字母、數字和連字號
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")


def generate_drug_news_page(slug: str, drug_info: dict, drug_detail: dict, drug_search: dict, news_items: list[dict]):
    """產生藥物新聞頁面"""
    name = drug_info.get("name", slug)
    original_indication = drug_detail.get("original_indication", "")
    evidence_level = drug_detail.get("evidence_level", "")
    indications = drug_search.get("indications", [])

    # 收集有新聞的適應症（英文名 -> 在地關鍵字）
    matched_indications = {}
    for item in news_items:
        for match in item.get("matched_keywords", []):
            if match.get("type") == "indication":
                en_name = match.get("name", "")
                loc_keyword = match.get("keyword", en_name)
                matched_indications[en_name] = loc_keyword

    desc_indication = original_indication[:50] + "..." if len(original_indication) > 50 else original_indication
    description = N["desc_drug"].format(name=name, ind=desc_indication, m=len(indications))
    page_title = N["title_news"].format(name=name)

    content = f"""---
layout: default
title: "{page_title}"
parent: {NEWS_PARENT}
nav_exclude: true
description: "{description}"
permalink: /news/{slug}/
---

# {page_title}

[{N["back"]}]({{{{ '/news/' | relative_url }}}})

---

<p class="key-answer" data-question="{N["q"].format(name=name)}">
{N["sum_drug"].format(name=name, n=len(news_items), m=len(indications))}
</p>

<div class="key-takeaway">
{N["take_drug"].format(name=name)}
</div>

<div class="drug-info-card">
<strong>{N["drug_info"]}</strong>
<ul>
"""

    if original_indication:
        content += f"<li><strong>{N['orig_ind']}</strong>: {original_indication}</li>\n"
    if evidence_level:
        content += f"<li><strong>{N['ev_level']}</strong>: {evidence_level}</li>\n"

    # 列出預測適應症（有新聞的標記顏色）
    if indications:
        content += f"<li><strong>{N['pred_ind_h'].format(m=len(indications))}</strong>:<ul>\n"
        for ind in indications:
            ind_name = ind.get("name", "")
            ind_score = ind.get("score", 0)
            if ind_name in matched_indications:
                loc_keyword = matched_indications[ind_name]
                content += f'<li class="indication-matched">{ind_name} ({ind_score:.1f}%)<span class="indication-tag">📰 {loc_keyword}</span></li>\n'
            else:
                content += f"<li>{ind_name} ({ind_score:.1f}%)</li>\n"
        content += "</ul></li>\n"

    content += f"""</ul>
<p><a href="{{{{ '/drugs/{slug}/' | relative_url }}}}">{N["full_report"]}</a></p>
</div>

## {N["rel_news_h"].format(n=len(news_items))}

"""

    if news_items:
        for item in sorted(news_items, key=lambda x: x["published"], reverse=True):
            try:
                dt = datetime.fromisoformat(item["published"])
                date_str = dt.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                date_str = N["unknown_date"]

            sources = item.get("sources", [])
            first_link = sources[0]["link"] if sources else "#"
            sources_html = " · ".join(
                f'[{s["name"]}]({s["link"]})'
                for s in sources
            )

            keyword_tags = []
            for match in item.get("matched_keywords", []):
                if match.get("type") == "indication":
                    loc_keyword = match.get("keyword", match.get("name", ""))
                    keyword_tags.append(f'<span class="news-indication-tag">{loc_keyword}</span>')
                elif match.get("type") == "drug":
                    keyword_tags.append(f'<span class="news-drug-tag">{match.get("name", "")}</span>')
            keyword_html = " ".join(keyword_tags) if keyword_tags else ""

            content += f"""### [{item["title"]}]({first_link})

{date_str} {keyword_html}

{N["source"]}: {sources_html}

---

"""
    else:
        content += N["no_news"] + "\n\n"

    content += f"""
<div class="disclaimer">
<strong>{N["disc_label"]}</strong>: {N["disc_body"]}
</div>

<style>
.indication-matched {{
  background: #fff3e0;
  padding: 4px 8px;
  border-radius: 4px;
  border-left: 3px solid #ff9800;
}}
.indication-tag {{
  display: inline-block;
  background: #ff9800;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  margin-left: 8px;
}}
.news-indication-tag {{
  display: inline-block;
  background: #ff9800;
  color: white;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.85em;
  margin-left: 4px;
}}
.news-drug-tag {{
  display: inline-block;
  background: #1565c0;
  color: white;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.85em;
  margin-left: 4px;
}}
</style>
"""

    # 寫入檔案
    output_path = NEWS_COLLECTION_DIR / f"{slug}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_indication_news_page(name: str, news_items: list[dict], keywords: dict):
    """產生適應症新聞頁面"""
    slug = slugify(name)

    # 從新聞項目中找出在地語言關鍵字
    loc_keyword = name
    for item in news_items:
        for match in item.get("matched_keywords", []):
            if match.get("type") == "indication" and match.get("name") == name:
                if match.get("keyword"):
                    loc_keyword = match["keyword"]
                    break
        if loc_keyword != name:
            break

    related_drugs = set()
    for ind in keywords.get("indications", []):
        if ind["name"] == name:
            related_drugs.update(ind.get("related_drugs", []))
            break

    drugs_map = {d["slug"]: d for d in keywords.get("drugs", [])}

    # 標題：優先使用在地關鍵字，括號內顯示原名
    display_title = f"{loc_keyword} ({name})" if loc_keyword != name else name

    description = N["desc_ind"].format(title=display_title, n=len(news_items), m=len(related_drugs))
    page_title = N["title_news"].format(name=display_title)

    content = f"""---
layout: default
title: "{page_title}"
parent: {NEWS_PARENT}
nav_exclude: true
description: "{description}"
permalink: /news/{slug}/
---

# {page_title}

[{N["back"]}]({{{{ '/news/' | relative_url }}}})

---

<p class="key-answer" data-question="{N["q"].format(name=display_title)}">
{N["sum_ind"].format(title=display_title, n=len(news_items), m=len(related_drugs))}
</p>

<div class="key-takeaway">
{N["take_ind"].format(kw=loc_keyword, proj=PROJECT_NAME)}
</div>

"""

    if related_drugs:
        content += f"""<div class="related-drugs-card">
<strong>{N["rel_drugs"]}</strong>
<p>{N["rel_drugs_p"]}</p>
<ul>
"""
        for drug_slug in sorted(related_drugs):
            drug = drugs_map.get(drug_slug, {})
            drug_name = drug.get("name", drug_slug)
            content += f'<li><a href="{{{{ \'/drugs/{drug_slug}/\' | relative_url }}}}">{drug_name}</a></li>\n'

        content += "</ul>\n</div>\n\n"

    content += f"""## {N["rel_news_h"].format(n=len(news_items))}

"""

    for item in sorted(news_items, key=lambda x: x["published"], reverse=True):
        try:
            dt = datetime.fromisoformat(item["published"])
            date_str = dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            date_str = N["unknown_date"]

        sources = item.get("sources", [])
        first_link = sources[0]["link"] if sources else "#"
        sources_html = " · ".join(
            f'[{s["name"]}]({s["link"]})'
            for s in sources
        )

        content += f"""### [{item["title"]}]({first_link})

{date_str}

{N["source"]}: {sources_html}

---

"""

    content += f"""
<div class="disclaimer">
<strong>{N["disc_label"]}</strong>: {N["disc_body"]}
</div>
"""

    output_path = NEWS_COLLECTION_DIR / f"{slug}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_news_index(matched_news: list[dict]):
    """產生前端用的新聞索引 JSON"""
    # 只保留有匹配關鍵字的新聞
    indexed_news = [
        {
            "id": item["id"],
            "title": item["title"],
            "published": item["published"],
            "sources": item["sources"],
            "keywords": item["matched_keywords"]
        }
        for item in matched_news
        if item.get("matched_keywords")
    ]

    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "count": len(indexed_news),
        "news": indexed_news
    }

    output_path = DOCS_DIR / "data" / "news-index.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(output, output_path)
    print(f"  產生索引: {output_path}")


def main():
    print("處理新聞資料...")

    # 1. 載入所有來源
    print("\n載入來源檔案:")
    all_news = load_all_sources()
    print(f"  總計: {len(all_news)} 則")

    # 2. 過濾舊新聞
    print("\n過濾舊新聞:")
    all_news = filter_old_news(all_news)

    # 3. 去重
    print("\n跨站去重:")
    all_news = deduplicate_news(all_news)

    # 4. 載入關鍵字並匹配
    print("\n關鍵字匹配:")
    keywords = load_json(DATA_DIR / "keywords.json")
    drug_count = keywords.get('drug_count', len(keywords.get('drugs', [])))
    indication_count = keywords.get('indication_count', len(keywords.get('indications', [])))
    print(f"  關鍵字: {drug_count} 藥物 + {indication_count} 適應症")
    all_news = match_keywords(all_news, keywords)

    # 5. 輸出 matched_news.json
    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_count": len(all_news),
        "matched_count": sum(1 for n in all_news if n.get("matched_keywords")),
        "news": all_news
    }
    save_json(output, DATA_DIR / "matched_news.json")
    print(f"\n輸出: {DATA_DIR / 'matched_news.json'}")

    # 6. 產生頁面
    print("\n產生 Jekyll 頁面:")
    generate_news_pages(all_news, keywords)

    # 7. 產生索引
    generate_news_index(all_news)

    print("\n完成！")


if __name__ == "__main__":
    main()
