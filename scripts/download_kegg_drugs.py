#!/usr/bin/env python3
"""從 KEGG 下載日本藥品資料

使用 KEGG REST API 下載日本藥品資料並轉換為標準 JSON 格式。

使用方法:
    uv run python scripts/download_kegg_drugs.py

產生檔案:
    data/raw/jp_fda_drugs.json
"""

import json
import re
import time
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError


KEGG_BASE = "https://rest.kegg.jp"
RATE_LIMIT_DELAY = 0.35  # 3 requests per second limit


def get_drug_list() -> list[tuple[str, str]]:
    """取得所有日本藥品列表"""
    url = f"{KEGG_BASE}/list/drug_ja"
    print(f"取得藥品列表: {url}")

    with urlopen(url) as response:
        content = response.read().decode("utf-8")

    drugs = []
    for line in content.strip().split("\n"):
        if "\t" in line:
            drug_id, names = line.split("\t", 1)
            drug_id = drug_id.replace("dr_ja:", "")
            drugs.append((drug_id, names))

    return drugs


def parse_drug_entry(content: str) -> dict:
    """解析 KEGG 藥品條目"""
    data = {}
    current_field = None
    current_value = []

    for line in content.split("\n"):
        if not line:
            continue

        # 檢查是否為新欄位
        if line[0] != " " and line[0] != "\t":
            # 儲存前一個欄位
            if current_field:
                data[current_field] = "\n".join(current_value).strip()

            # 解析新欄位
            parts = line.split(None, 1)
            if len(parts) >= 1:
                current_field = parts[0]
                current_value = [parts[1]] if len(parts) > 1 else []
        else:
            # 續行
            current_value.append(line.strip())

    # 儲存最後一個欄位
    if current_field:
        data[current_field] = "\n".join(current_value).strip()

    return data


def extract_drug_info(drug_id: str, raw_data: dict) -> dict:
    """從原始資料提取標準化藥品資訊"""
    # 一般名 → 販売名 (brand name)
    names = raw_data.get("一般名", "")
    name_list = [n.strip() for n in names.split(";") if n.strip()]

    # 提取日文名和英文名
    jp_names = [n for n in name_list if not re.match(r"^[A-Za-z]", n)]
    en_names = [n for n in name_list if re.match(r"^[A-Za-z]", n)]

    brand_name_local = jp_names[0] if jp_names else ""
    brand_name_en = en_names[0] if en_names else ""

    # 商品名
    brand_names = raw_data.get("商品名", "")

    # 効能 (indications)
    efficacy = raw_data.get("効能", "")

    # 疾患 (diseases)
    diseases = raw_data.get("疾患", "")
    if diseases:
        # 移除 [DS:...] 標記
        diseases = re.sub(r"\s*\[DS:[^\]]+\]", "", diseases)

    # 合併効能和疾患作為適應症
    indication_parts = []
    if efficacy:
        indication_parts.append(efficacy)
    if diseases:
        indication_parts.append(diseases)
    indication = "; ".join(indication_parts)

    # 組成式 / 分子式
    formula = raw_data.get("組成式", "") or raw_data.get("分子式", "")

    # 分子量
    mol_weight = raw_data.get("分子量", "")

    # 薬効分類
    drug_class = raw_data.get("クラス", "")

    # ATC コード
    codes = raw_data.get("コード", "")
    atc_match = re.search(r"ATCコード:\s*([A-Z]\d{2}[A-Z]{2}\d{2})", codes)
    atc_code = atc_match.group(1) if atc_match else ""

    return {
        "承認番号": drug_id,
        "販売名": brand_name_local,
        "一般名": brand_name_en,
        "有効成分": brand_name_en or brand_name_local,  # 使用名稱作為成分
        "効能・効果": indication,
        "剤形": "",
        "製造販売業者": "",
        "承認日": "",
        "承認状況": "有効",
        "商品名一覧": brand_names,
        "分子式": formula,
        "分子量": mol_weight,
        "薬効分類": drug_class,
        "ATCコード": atc_code,
    }


def download_drug_details(drug_ids: list[str], batch_size: int = 10) -> list[dict]:
    """批次下載藥品詳細資料"""
    drugs = []
    total = len(drug_ids)

    for i in range(0, total, batch_size):
        batch = drug_ids[i:i+batch_size]
        batch_str = "+".join([f"dr_ja:{d}" for d in batch])
        url = f"{KEGG_BASE}/get/{batch_str}"

        try:
            with urlopen(url) as response:
                content = response.read().decode("utf-8")

            # 分割多個條目 (以 /// 分隔)
            entries = content.split("///")

            for entry in entries:
                entry = entry.strip()
                if not entry:
                    continue

                raw_data = parse_drug_entry(entry)

                # 提取 drug_id
                entry_line = raw_data.get("エントリ", "")
                match = re.match(r"(D\d+)", entry_line)
                if match:
                    drug_id = match.group(1)
                    drug_info = extract_drug_info(drug_id, raw_data)
                    drugs.append(drug_info)

        except HTTPError as e:
            print(f"  HTTP 錯誤 ({i+1}-{i+len(batch)}): {e}")
        except Exception as e:
            print(f"  錯誤 ({i+1}-{i+len(batch)}): {e}")

        # 進度顯示
        progress = min(i + batch_size, total)
        if progress % 100 == 0 or progress == total:
            print(f"  已下載: {progress}/{total} ({progress*100/total:.1f}%)", flush=True)

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

    return drugs


def main():
    import sys
    print("=" * 60, flush=True)
    print("從 KEGG 下載日本藥品資料", flush=True)
    print("=" * 60, flush=True)
    print(flush=True)

    base_dir = Path(__file__).parent.parent
    output_path = base_dir / "data" / "raw" / "jp_kegg_drugs.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 取得藥品列表
    print("步驟 1: 取得藥品列表...", flush=True)
    drug_list = get_drug_list()
    drug_ids = [d[0] for d in drug_list]
    print(f"  共 {len(drug_ids)} 個藥品", flush=True)

    # 下載詳細資料
    print()
    print("步驟 2: 下載藥品詳細資料...")
    print("  (KEGG API 限制: 每秒 3 次請求)")
    drugs = download_drug_details(drug_ids)

    # 儲存結果
    print()
    print("步驟 3: 儲存結果...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(drugs, f, ensure_ascii=False, indent=2)

    print(f"  已儲存至: {output_path}")
    print(f"  共 {len(drugs)} 筆藥品資料")

    # 統計
    with_indication = sum(1 for d in drugs if d.get("効能・効果"))
    print()
    print("統計:")
    print(f"  有適應症資料: {with_indication} ({with_indication*100/len(drugs):.1f}%)")


if __name__ == "__main__":
    main()
