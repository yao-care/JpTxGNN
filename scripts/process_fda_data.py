#!/usr/bin/env python3
"""處理日本 PMDA 藥品資料

將下載的 PMDA 藥品資料檔案轉換為標準 JSON 格式。

使用方法:
    uv run python scripts/process_fda_data.py

前置條件:
    需要先下載 PMDA 資料檔案到 data/raw/ 目錄
    https://www.pmda.go.jp/

產生檔案:
    data/raw/jp_fda_drugs.json
"""

import csv
import json
import zipfile
from pathlib import Path


def find_data_file(raw_dir: Path) -> Path:
    """在 raw 目錄中尋找資料檔案

    Args:
        raw_dir: data/raw/ 目錄路徑

    Returns:
        找到的資料檔案路徑

    Raises:
        FileNotFoundError: 找不到資料檔案
    """
    # 尋找 ZIP、JSON 或 CSV 檔案
    for pattern in ["*.zip", "*.json", "*.csv"]:
        data_files = list(raw_dir.glob(pattern))
        if data_files:
            return data_files[0]

    raise FileNotFoundError(
        f"在 {raw_dir} 找不到資料檔案\n"
        f"請先從以下網址下載 PMDA 資料並放到 data/raw/ 目錄：\n"
        f"https://www.pmda.go.jp/"
    )


def process_data_file(input_path: Path, output_path: Path) -> Path:
    """處理資料檔案並轉換為 JSON

    Args:
        input_path: 輸入檔案路徑
        output_path: 輸出 JSON 檔案路徑

    Returns:
        輸出檔案路徑
    """
    print(f"讀取資料檔案: {input_path}")
    print(f"檔案大小: {input_path.stat().st_size / 1024 / 1024:.1f} MB")

    data = []

    if input_path.suffix == ".zip":
        print("解壓縮中...")
        with zipfile.ZipFile(input_path, 'r') as zf:
            # 優先尋找 JSON
            json_files = [f for f in zf.namelist() if f.endswith('.json')]
            csv_files = [f for f in zf.namelist() if f.endswith('.csv')]

            if json_files:
                with zf.open(json_files[0]) as f:
                    content = f.read()
                    # 嘗試 UTF-8，若失敗則嘗試 Shift-JIS
                    try:
                        data = json.loads(content.decode('utf-8'))
                    except UnicodeDecodeError:
                        data = json.loads(content.decode('shift-jis'))
            elif csv_files:
                with zf.open(csv_files[0]) as f:
                    try:
                        content = f.read().decode('utf-8')
                    except UnicodeDecodeError:
                        content = f.read().decode('shift-jis')
                    reader = csv.DictReader(content.splitlines())
                    data = list(reader)
            else:
                raise ValueError("ZIP 檔案中找不到 JSON 或 CSV 檔案")

    elif input_path.suffix == ".json":
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except UnicodeDecodeError:
            with open(input_path, "r", encoding="shift-jis") as f:
                data = json.load(f)

    elif input_path.suffix == ".csv":
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data = list(reader)
        except UnicodeDecodeError:
            with open(input_path, "r", encoding="shift-jis") as f:
                reader = csv.DictReader(f)
                data = list(reader)

    else:
        raise ValueError(f"不支援的檔案格式: {input_path.suffix}")

    # 確保輸出目錄存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 儲存 JSON
    print(f"儲存至: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"完成！共 {len(data)} 筆藥品資料")
    return output_path


def main():
    print("=" * 60)
    print("處理日本 PMDA 藥品資料")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent.parent
    raw_dir = base_dir / "data" / "raw"
    output_path = raw_dir / "jp_fda_drugs.json"

    raw_dir.mkdir(parents=True, exist_ok=True)

    input_path = find_data_file(raw_dir)
    process_data_file(input_path, output_path)

    print()
    print("下一步: 準備詞彙表資料")
    print("  uv run python scripts/prepare_external_data.py")


if __name__ == "__main__":
    main()
