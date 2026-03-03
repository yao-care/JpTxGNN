#!/usr/bin/env python3
"""
ニュース処理スクリプト

機能：
1. data/news/*.json から全ソースファイルを読み込み
2. keywords.json でキーワードマッチング
3. 重複削除（類似タイトルをマージ）
4. matched_news.json を出力
5. docs/_news/*.md ページを生成
"""

import json
import re
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path

# プロジェクトルートディレクトリ
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "news"
DOCS_DIR = PROJECT_ROOT / "docs"
NEWS_COLLECTION_DIR = DOCS_DIR / "_news"

# 設定
SIMILARITY_THRESHOLD = 0.8  # タイトル類似度閾値
TIME_WINDOW_HOURS = 24  # 重複検出時間ウィンドウ（時間）
MAX_NEWS_AGE_DAYS = 30  # 最大ニュース保持日数


def load_json(path: Path) -> dict | list:
    """JSONファイルを読み込む"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict | list, path: Path):
    """JSONファイルを保存"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_all_sources() -> list[dict]:
    """全ソースからニュースを読み込む"""
    all_news = []
    excluded = {"keywords.json", "matched_news.json", "synonyms.json"}

    for json_file in DATA_DIR.glob("*.json"):
        if json_file.name in excluded:
            continue

        try:
            data = load_json(json_file)
            source_name = data.get("source", json_file.stem)
            news_items = data.get("news", [])
            print(f"  - {json_file.name}: {len(news_items)} 件")

            for item in news_items:
                item["_source_file"] = source_name
                all_news.append(item)

        except Exception as e:
            print(f"  警告: {json_file.name} の読み込みに失敗 - {e}")

    return all_news


def filter_old_news(news_items: list[dict]) -> list[dict]:
    """30日以上前の古いニュースをフィルタリング"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_NEWS_AGE_DAYS)
    filtered = []

    for item in news_items:
        try:
            published = datetime.fromisoformat(item.get("published", ""))
            if published >= cutoff:
                filtered.append(item)
        except (ValueError, TypeError):
            # 日付解析不可、保持
            filtered.append(item)

    removed = len(news_items) - len(filtered)
    if removed > 0:
        print(f"  古いニュースをフィルタリング: {removed} 件")

    return filtered


def title_similarity(title1: str, title2: str) -> float:
    """2つのタイトルの類似度を計算"""
    # ソースマーク（「- Yahoo!ニュース」など）を削除
    clean1 = re.sub(r"\s*[-–—]\s*[^\s]+$", "", title1).strip()
    clean2 = re.sub(r"\s*[-–—]\s*[^\s]+$", "", title2).strip()

    return SequenceMatcher(None, clean1, clean2).ratio()


def deduplicate_news(news_items: list[dict]) -> list[dict]:
    """重複削除、類似ニュースのソースをマージ"""
    # 公開日でソート（最新が先）
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

        # 類似ニュースを検索
        similar_items = [item]
        item_time = datetime.fromisoformat(
            item.get("published", datetime.now(timezone.utc).isoformat())
        )

        for j, other in enumerate(sorted_news[i + 1:], start=i + 1):
            if j in used_indices:
                continue

            # 時間ウィンドウをチェック
            other_time = datetime.fromisoformat(
                other.get("published", datetime.now(timezone.utc).isoformat())
            )
            time_diff = abs((item_time - other_time).total_seconds() / 3600)

            if time_diff > TIME_WINDOW_HOURS:
                continue

            # タイトル類似度をチェック
            if title_similarity(item["title"], other["title"]) >= SIMILARITY_THRESHOLD:
                similar_items.append(other)
                used_indices.add(j)

        # ソースをマージ
        all_sources = []
        seen_links = set()
        for sim_item in similar_items:
            for source in sim_item.get("sources", []):
                if source["link"] not in seen_links:
                    seen_links.add(source["link"])
                    all_sources.append(source)

        # 最も早い公開時間を使用
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
            "matched_keywords": []  # 後で追加
        }
        merged.append(merged_item)
        used_indices.add(i)

    print(f"  重複削除後: {len(merged)} 件（{len(news_items) - len(merged)} 件マージ）")
    return merged


def match_keywords(news_items: list[dict], keywords: dict) -> list[dict]:
    """ニュースにキーワードマッチング"""
    drugs = keywords.get("drugs", [])
    indications = keywords.get("indications", [])

    # 薬物 slug -> name のマップを構築
    drug_name_map = {d["slug"]: d["name"] for d in drugs}

    matched_count = 0

    for item in news_items:
        text_to_search = f"{item['title']} {item.get('summary', '')}".lower()
        matches = []

        # 薬物をマッチング
        for drug in drugs:
            drug_name = drug["name"]
            drug_slug = drug["slug"]

            # 英語キーワード
            for kw in drug["keywords"].get("en", []):
                if kw.lower() in text_to_search:
                    matches.append({
                        "type": "drug",
                        "slug": drug_slug,
                        "keyword": kw,
                        "name": drug_name,
                        "url": drug["url"]
                    })
                    break  # 同一薬物は1回のみ記録

            # 日本語キーワード
            for kw in drug["keywords"].get("ja", []):
                if kw in item["title"] or kw in item.get("summary", ""):
                    # 重複を避ける
                    if not any(m["slug"] == drug_slug for m in matches):
                        matches.append({
                            "type": "drug",
                            "slug": drug_slug,
                            "keyword": kw,
                            "name": drug_name,
                            "url": drug["url"]
                        })
                    break

        # 適応症をマッチング
        for ind in indications:
            ind_name = ind["name"]

            # related_drugs を slug から {slug, name} 形式に変換
            related_drugs = [
                {"slug": slug, "name": drug_name_map.get(slug, slug)}
                for slug in ind.get("related_drugs", [])
            ]

            # 英語キーワード
            for kw in ind["keywords"].get("en", []):
                if kw.lower() in text_to_search:
                    matches.append({
                        "type": "indication",
                        "name": ind_name,
                        "keyword": kw,
                        "related_drugs": related_drugs
                    })
                    break

            # 日本語キーワード
            for kw in ind["keywords"].get("ja", []):
                if kw in item["title"] or kw in item.get("summary", ""):
                    # 同一キーワードの重複を避ける
                    if not any(m.get("keyword") == kw and m["type"] == "indication" for m in matches):
                        matches.append({
                            "type": "indication",
                            "name": ind_name,
                            "keyword": kw,
                            "related_drugs": related_drugs
                        })
                    break

        item["matched_keywords"] = matches
        if matches:
            matched_count += 1

    print(f"  キーワードマッチ: {matched_count} 件")
    return news_items


def generate_news_index(matched_news: list[dict]):
    """フロントエンド用のニュースインデックスJSONを生成"""
    # マッチしたキーワードがあるニュースのみ保持
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
    print(f"  インデックス生成: {output_path}")


def main():
    print("ニュースデータを処理中...")

    # 1. 全ソースを読み込む
    print("\nソースファイルを読み込み:")
    all_news = load_all_sources()
    print(f"  合計: {len(all_news)} 件")

    if not all_news:
        print("  ニュースデータがありません。scripts/fetchers/japan_news.py を先に実行してください。")
        return

    # 2. 古いニュースをフィルタリング
    print("\n古いニュースをフィルタリング:")
    all_news = filter_old_news(all_news)

    # 3. 重複削除
    print("\n重複削除:")
    all_news = deduplicate_news(all_news)

    # 4. キーワードを読み込んでマッチング
    keywords_path = DATA_DIR / "keywords.json"
    if not keywords_path.exists():
        print(f"  警告: {keywords_path} が見つかりません。scripts/generate_news_keywords.py を先に実行してください。")
        return

    print("\nキーワードマッチング:")
    keywords = load_json(keywords_path)
    print(f"  キーワード: {keywords['drug_count']} 薬物 + {keywords['indication_count']} 適応症")
    all_news = match_keywords(all_news, keywords)

    # 5. matched_news.json を出力
    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_count": len(all_news),
        "matched_count": sum(1 for n in all_news if n.get("matched_keywords")),
        "news": all_news
    }
    save_json(output, DATA_DIR / "matched_news.json")
    print(f"\n出力: {DATA_DIR / 'matched_news.json'}")
    print(f"  合計: {output['total_count']} 件")
    print(f"  マッチ: {output['matched_count']} 件")

    # 6. インデックスを生成
    print("\nインデックス生成:")
    generate_news_index(all_news)

    print("\n完了！")


if __name__ == "__main__":
    main()
