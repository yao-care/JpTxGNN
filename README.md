# JpTxGNN - 日本 PMDA 医薬品リポジショニング予測システム

TxGNN 知識グラフを使用した日本の医薬品リポジショニング（ドラッグリポジショニング）予測システム。

## 免責事項

本プロジェクトの結果は研究参考のみを目的としており、医療アドバイスを構成するものではありません。
医薬品リポジショニング候補は臨床検証を経て初めて適用できます。

## 使用方法

```bash
# 依存関係をインストール
uv sync

# PMDA データを処理
uv run python scripts/process_fda_data.py

# 外部データを準備
uv run python scripts/prepare_external_data.py

# KG 予測を実行
uv run python scripts/run_kg_prediction.py

# FHIR リソースを生成
uv run python scripts/generate_fhir_resources.py
```

## ライセンス

研究目的のみ使用可能。
