#!/usr/bin/env python3
"""將 SSK 藥價マスター轉換為標準 JSON 格式

使用方法:
    uv run python scripts/convert_ssk_to_json.py

輸入:
    data/raw/y_ALL20260219_utf8.csv

產生檔案:
    data/raw/jp_fda_drugs.json
"""

import csv
import json
import re
from pathlib import Path


def parse_drug_name(raw_name: str) -> tuple[str, str]:
    """解析藥品名稱，分離一般名和劑量/規格

    例: "ガスター散２％" -> ("ガスター", "散２％")
    """
    # 常見劑型後綴
    forms = [
        "錠", "カプセル", "散", "顆粒", "細粒", "注射液", "注射用", "注",
        "液", "シロップ", "点眼液", "点鼻液", "軟膏", "クリーム", "テープ",
        "パップ", "ゲル", "ローション", "吸入", "噴霧", "坐剤", "坐薬"
    ]

    name = raw_name
    form = ""

    # 嘗試分離劑型
    for f in forms:
        if f in name:
            idx = name.find(f)
            form = name[idx:]
            name = name[:idx]
            break

    return name.strip(), form.strip()


def extract_generic_name(name: str, kana: str) -> str:
    """提取藥品通用名（用於 DrugBank 映射）

    優先使用英文/片假名名稱
    """
    # 嘗試從名稱中提取英文部分
    en_match = re.search(r'[A-Za-z][A-Za-z0-9\-]+', name)
    if en_match:
        return en_match.group()

    # 使用片假名
    if kana:
        # 移除劑型後綴
        kana_clean = re.sub(r'(ｻﾝ|ｻﾞｲ|ｼﾞｮｳ|ｶﾌﾟｾﾙ|ﾁｭｳｼｬ|ﾃﾝｶﾞﾝ).*$', '', kana)
        return kana_clean

    return name


def convert_ssk_to_json(input_path: Path, output_path: Path):
    """轉換 SSK 藥價マスター CSV 為 JSON"""

    drugs = []

    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 38:
                continue

            # SSK 欄位對應 (根據實際資料結構)
            # [2] 藥品代碼
            # [4] 品名
            # [6] 片假名品名
            # [9] 單位
            # [11] 藥價
            # [29] 有効開始日
            # [30] 有効終了日
            # [31] 薬価基準コード
            # [37] 一般名（【般】前綴）

            try:
                drug_code = row[2]
                brand_name = row[4]
                kana_name = row[6]
                unit = row[9] if len(row) > 9 else ""
                price = row[11] if len(row) > 11 else ""
                start_date = row[29] if len(row) > 29 else ""
                end_date = row[30] if len(row) > 30 else ""
                yj_code = row[31] if len(row) > 31 else ""
                generic_raw = row[37] if len(row) > 37 else ""

                # 跳過無效記錄
                if not brand_name:
                    continue

                # 解析一般名（移除【般】前綴）
                generic_name = re.sub(r'^【般】', '', generic_raw).strip()

                # 解析名稱
                base_name, form = parse_drug_name(brand_name)

                # 提取有效成分（從一般名或品名）
                if generic_name:
                    ingredient = extract_generic_name(generic_name, "")
                else:
                    ingredient = extract_generic_name(base_name, kana_name)

                # 判斷狀態
                status = "有効"
                if end_date and end_date != "99999999":
                    status = "販売中止"

                drug = {
                    "承認番号": drug_code,
                    "販売名": brand_name,
                    "一般名": generic_name,
                    "有効成分": ingredient,
                    "効能・効果": "",  # SSK 沒有適應症資料
                    "剤形": form,
                    "製造販売業者": "",
                    "承認日": start_date,
                    "承認状況": status,
                    "薬価": price,
                    "単位": unit,
                    "薬価基準コード": yj_code,
                }

                drugs.append(drug)

            except (IndexError, ValueError) as e:
                continue

    # 儲存 JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(drugs, f, ensure_ascii=False, indent=2)

    return drugs


def main():
    print("=" * 60)
    print("轉換 SSK 藥價マスター為 JSON")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent.parent
    input_path = base_dir / "data" / "raw" / "y_ALL20260219_utf8.csv"
    output_path = base_dir / "data" / "raw" / "jp_fda_drugs.json"

    if not input_path.exists():
        print(f"錯誤: 找不到輸入檔案 {input_path}")
        return

    print(f"輸入: {input_path}")
    print(f"輸出: {output_path}")
    print()

    drugs = convert_ssk_to_json(input_path, output_path)

    print(f"完成！共 {len(drugs)} 筆藥品")

    # 顯示範例
    print()
    print("範例資料:")
    for drug in drugs[:3]:
        print(f"  - {drug['販売名']} ({drug['有効成分']})")


if __name__ == "__main__":
    main()
