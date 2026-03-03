#!/usr/bin/env python3
"""
Japan Health News Fetcher

日本の健康ニュースを収集:
- Google News Japan 健康カテゴリ
- Yahoo! Japan ヘルスケアニュース

出力: data/news/japan_news.json
"""

import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import feedparser

# プロジェクトルートディレクトリ
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "news"

# Google News Japan 健康カテゴリ RSS
# トピック ID は健康カテゴリを示す
GOOGLE_NEWS_HEALTH_RSS = (
    "https://news.google.com/rss/topics/"
    "CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JYcG9MVXBRS0FBUAE"
    "?hl=ja&gl=JP&ceid=JP:ja"
)

# Yahoo! Japan ニュース 科学・IT RSS (医療ニュースを含む)
YAHOO_JAPAN_SCIENCE_RSS = "https://news.yahoo.co.jp/rss/categories/science.xml"

# Yahoo! Japan ニュース ライフ RSS (健康ニュースを含む)
YAHOO_JAPAN_LIFE_RSS = "https://news.yahoo.co.jp/rss/categories/life.xml"

# レート制限
REQUEST_DELAY = 1.0  # 秒


def generate_id(title: str, link: str) -> str:
    """ニュースID生成（タイトルとリンクのハッシュに基づく）"""
    content = f"{title}:{link}"
    return hashlib.md5(content.encode()).hexdigest()[:12]


def parse_source(entry, default_source: str = "Unknown") -> dict:
    """RSSエントリからソース情報を抽出"""
    source_name = default_source
    if hasattr(entry, "source") and hasattr(entry.source, "title"):
        source_name = entry.source.title

    return {
        "name": source_name,
        "link": entry.get("link", "")
    }


def parse_published(entry) -> str:
    """公開時間を解析し、ISO 8601形式に変換"""
    published = entry.get("published_parsed")
    if published:
        try:
            dt = datetime(*published[:6], tzinfo=timezone.utc)
            return dt.isoformat()
        except Exception:
            pass

    # 解析に失敗した場合、現在時刻を使用
    return datetime.now(timezone.utc).isoformat()


def clean_summary(summary: str) -> str:
    """要約テキストをクリーンアップ（HTMLタグを削除等）"""
    # HTMLタグを削除
    clean = re.sub(r"<[^>]+>", "", summary)
    # 余分な空白を削除
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean[:500] if len(clean) > 500 else clean


def fetch_rss(url: str, source_name: str) -> list[dict]:
    """RSS URLからニュースをフェッチ"""
    print(f"  フェッチ中: {source_name}")
    print(f"    URL: {url[:70]}...")

    try:
        # カスタムヘッダーでフェッチ
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; JpTxGNN/1.0; +https://jptxgnn.yao.care)",
            "Accept": "application/rss+xml, application/xml, text/xml",
            "Accept-Language": "ja,en;q=0.9",
        }
        request = Request(url, headers=headers)
        with urlopen(request, timeout=30) as response:
            content = response.read()
    except (HTTPError, URLError) as e:
        print(f"    エラー: {e}")
        return []

    feed = feedparser.parse(content)

    if feed.bozo:
        print(f"    警告: RSS解析に問題あり - {feed.bozo_exception}")

    news_items = []

    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")

        if not title or not link:
            continue

        news_id = generate_id(title, link)
        source = parse_source(entry, source_name)
        published = parse_published(entry)
        summary = clean_summary(entry.get("summary", "") or entry.get("description", ""))

        news_items.append({
            "id": news_id,
            "title": title,
            "published": published,
            "summary": summary,
            "sources": [source]
        })

    print(f"    取得: {len(news_items)} 件のニュース")
    return news_items


def fetch_google_news_japan() -> list[dict]:
    """Google News Japan 健康カテゴリをフェッチ"""
    return fetch_rss(GOOGLE_NEWS_HEALTH_RSS, "Google News Japan")


def fetch_yahoo_japan_science() -> list[dict]:
    """Yahoo! Japan 科学ニュースをフェッチ"""
    return fetch_rss(YAHOO_JAPAN_SCIENCE_RSS, "Yahoo! Japan Science")


def fetch_yahoo_japan_life() -> list[dict]:
    """Yahoo! Japan ライフニュースをフェッチ"""
    return fetch_rss(YAHOO_JAPAN_LIFE_RSS, "Yahoo! Japan Life")


def deduplicate_news(news_items: list[dict]) -> list[dict]:
    """重複ニュースを削除（IDベース）"""
    seen_ids = set()
    unique_items = []

    for item in news_items:
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            unique_items.append(item)

    return unique_items


def filter_health_keywords(news_items: list[dict]) -> list[dict]:
    """健康関連のキーワードでフィルタリング"""
    health_keywords = [
        # 医療・健康
        "医療", "医薬", "薬", "治療", "診断", "手術", "病院", "クリニック",
        "健康", "病気", "疾患", "症状", "感染", "ウイルス", "細菌",
        # 疾患名
        "がん", "癌", "糖尿病", "高血圧", "心臓", "脳卒中", "認知症",
        "うつ", "不眠", "喘息", "アレルギー", "肝炎", "腎臓",
        # 薬・治療法
        "新薬", "治験", "臨床試験", "承認", "FDA", "PMDA",
        "ワクチン", "抗体", "免疫", "遺伝子", "iPS", "再生医療",
        # 研究
        "研究", "発見", "開発", "効果", "副作用", "リスク",
    ]

    filtered = []
    for item in news_items:
        text = f"{item['title']} {item.get('summary', '')}"
        if any(keyword in text for keyword in health_keywords):
            filtered.append(item)

    return filtered


def main():
    print("日本の健康ニュースを収集中...")

    # ディレクトリを確保
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_news = []

    # Google News Japan
    news = fetch_google_news_japan()
    all_news.extend(news)
    time.sleep(REQUEST_DELAY)

    # Yahoo! Japan Science
    news = fetch_yahoo_japan_science()
    all_news.extend(news)
    time.sleep(REQUEST_DELAY)

    # Yahoo! Japan Life
    news = fetch_yahoo_japan_life()
    all_news.extend(news)

    # 重複削除
    unique_news = deduplicate_news(all_news)
    print(f"\n重複削除後: {len(unique_news)} 件")

    # 健康関連フィルタリング
    health_news = filter_health_keywords(unique_news)
    print(f"健康関連フィルタリング後: {len(health_news)} 件")

    # 公開日でソート（新しい順）
    health_news.sort(key=lambda x: x["published"], reverse=True)

    # 出力
    output = {
        "source": "japan_news",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_fetched": len(all_news),
        "unique_count": len(unique_news),
        "health_related_count": len(health_news),
        "news": health_news
    }

    output_path = DATA_DIR / "japan_news.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n出力: {output_path}")
    print(f"  - 総フェッチ数: {len(all_news)}")
    print(f"  - ユニーク数: {len(unique_news)}")
    print(f"  - 健康関連: {len(health_news)}")


if __name__ == "__main__":
    main()
