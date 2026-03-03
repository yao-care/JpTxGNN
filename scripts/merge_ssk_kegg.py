#!/usr/bin/env python3
"""合併 SSK 藥價資料和 KEGG 適應症資料

策略：
1. 以 SSK 為主體（藥品較多，含藥價資訊）
2. 從 KEGG 補充適應症資料（効能・効果）
3. 透過藥品名稱匹配

使用方法:
    uv run python scripts/merge_ssk_kegg.py
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional


def normalize_drug_name(name: str) -> str:
    """標準化藥品名稱以便比對"""
    if not name:
        return ""
    # 移除數字、符號
    name = re.sub(r'[０-９0-9．.]+', '', name)
    # 移除劑型後綴
    name = re.sub(r'(％|%|ｇ|g|mg|μｇ|μg|mL|ｍＬ|錠|散|液|注射|剤|注|カプセル|顆粒|細粒|軟膏|クリーム|ゲル|テープ|パップ|シロップ|点眼|吸入|坐).*$', '', name)
    # 移除空格
    name = re.sub(r'\s+', '', name)
    # 移除括號及其內容
    name = re.sub(r'[\(（][^\)）]*[\)）]', '', name)
    return name.strip()


def extract_base_ingredient(name: str) -> str:
    """提取基本成分名（移除更多後綴）"""
    if not name:
        return ""
    # 先做基本標準化
    base = normalize_drug_name(name)
    # 移除鹽類後綴
    salt_patterns = [
        r'ナトリウム$', r'カリウム$', r'カルシウム$', r'マグネシウム$',
        r'塩酸塩$', r'硫酸塩$', r'酢酸塩$', r'クエン酸塩$',
        r'メシル酸塩$', r'マレイン酸塩$', r'フマル酸塩$',
        r'水和物$', r'無水物$',
    ]
    for pattern in salt_patterns:
        base = re.sub(pattern, '', base)
    return base.strip()


def build_kegg_index(kegg_drugs: list) -> Dict[str, dict]:
    """建立 KEGG 藥品索引（多種鍵值）"""
    index = {}

    for drug in kegg_drugs:
        keys_to_add = []

        # 索引：承認番号（KEGG ID like D00001）
        if drug.get("承認番号"):
            keys_to_add.append(drug["承認番号"])

        # 索引：販売名（標準化）
        if drug.get("販売名"):
            keys_to_add.append(normalize_drug_name(drug["販売名"]))
            keys_to_add.append(extract_base_ingredient(drug["販売名"]))

        # 索引：一般名（可能有多個名稱，用 ; 或 / 分隔）
        if drug.get("一般名"):
            for sep in [";", "/"]:
                for name in drug["一般名"].split(sep):
                    name = name.strip()
                    if name:
                        keys_to_add.append(normalize_drug_name(name))
                        keys_to_add.append(extract_base_ingredient(name))
                        # 也加入原始名稱的大寫形式
                        keys_to_add.append(name.upper().strip())

        # 索引：有効成分
        if drug.get("有効成分"):
            keys_to_add.append(normalize_drug_name(drug["有効成分"]))
            keys_to_add.append(extract_base_ingredient(drug["有効成分"]))

        # 加入索引
        for key in keys_to_add:
            if key and key not in index:
                index[key] = drug

    return index


def find_kegg_match(ssk_drug: dict, kegg_index: Dict[str, dict]) -> Optional[dict]:
    """從 KEGG 索引中尋找匹配的藥品"""
    keys_to_try = []

    # 收集所有可能的匹配鍵
    for field in ["一般名", "販売名", "有効成分"]:
        if ssk_drug.get(field):
            value = ssk_drug[field]
            keys_to_try.append(normalize_drug_name(value))
            keys_to_try.append(extract_base_ingredient(value))
            keys_to_try.append(value.upper().strip())

    # 依序嘗試匹配
    for key in keys_to_try:
        if key and key in kegg_index:
            return kegg_index[key]

    return None


def merge_drug_data(ssk_drug: dict, kegg_drug: Optional[dict]) -> dict:
    """合併單一藥品資料"""
    merged = ssk_drug.copy()

    if kegg_drug:
        # 從 KEGG 補充缺少的欄位
        if not merged.get("効能・効果") and kegg_drug.get("効能・効果"):
            merged["効能・効果"] = kegg_drug["効能・効果"]

        if not merged.get("商品名一覧") and kegg_drug.get("商品名一覧"):
            merged["商品名一覧"] = kegg_drug["商品名一覧"]

        if not merged.get("分子式") and kegg_drug.get("分子式"):
            merged["分子式"] = kegg_drug["分子式"]

        if not merged.get("分子量") and kegg_drug.get("分子量"):
            merged["分子量"] = kegg_drug["分子量"]

        if not merged.get("薬効分類") and kegg_drug.get("薬効分類"):
            merged["薬効分類"] = kegg_drug["薬効分類"]

        if not merged.get("ATCコード") and kegg_drug.get("ATCコード"):
            merged["ATCコード"] = kegg_drug["ATCコード"]

        # 標記來源
        merged["KEGG_ID"] = kegg_drug.get("承認番号", "")

    return merged


def main():
    print("=" * 60)
    print("合併 SSK 藥價資料和 KEGG 適應症資料")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent.parent
    ssk_path = base_dir / "data" / "raw" / "jp_ssk_drugs.json"
    kegg_path = base_dir / "data" / "raw" / "jp_kegg_drugs.json"
    output_path = base_dir / "data" / "raw" / "jp_fda_drugs.json"

    # 讀取資料
    print("步驟 1: 讀取資料...")
    with open(ssk_path, "r", encoding="utf-8") as f:
        ssk_drugs = json.load(f)
    print(f"  SSK 藥品數: {len(ssk_drugs)}")

    with open(kegg_path, "r", encoding="utf-8") as f:
        kegg_drugs = json.load(f)
    print(f"  KEGG 藥品數: {len(kegg_drugs)}")

    # 建立 KEGG 索引
    print()
    print("步驟 2: 建立 KEGG 索引...")
    kegg_index = build_kegg_index(kegg_drugs)
    print(f"  索引項目數: {len(kegg_index)}")

    # 合併資料
    print()
    print("步驟 3: 合併資料...")
    merged_drugs = []
    matched_count = 0

    for ssk_drug in ssk_drugs:
        kegg_match = find_kegg_match(ssk_drug, kegg_index)
        merged = merge_drug_data(ssk_drug, kegg_match)
        merged_drugs.append(merged)
        if kegg_match:
            matched_count += 1

    print(f"  成功匹配: {matched_count} ({matched_count*100/len(ssk_drugs):.1f}%)")

    # 統計
    with_indication = sum(1 for d in merged_drugs if d.get("効能・効果"))
    print(f"  有適應症: {with_indication} ({with_indication*100/len(merged_drugs):.1f}%)")

    # 儲存
    print()
    print("步驟 4: 儲存結果...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged_drugs, f, ensure_ascii=False, indent=2)
    print(f"  已儲存至: {output_path}")

    # 顯示範例
    print()
    print("範例資料（有適應症）:")
    for drug in merged_drugs:
        if drug.get("効能・効果"):
            print(f"  - {drug['販売名']}")
            print(f"    適應症: {drug['効能・効果'][:50]}...")
            break

    print()
    print("完成！")


if __name__ == "__main__":
    main()
