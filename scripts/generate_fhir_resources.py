#!/usr/bin/env python3
"""
FHIR R4 リソースを JpTxGNN 医薬品予測データから生成

このスクリプトは以下を生成:
- 各医薬品の MedicationKnowledge リソース
- 各予測適応症の ClinicalUseDefinition リソース
- 全リソースを含む Bundle
- CapabilityStatement (metadata)
"""

import json
import re
from datetime import datetime
from pathlib import Path


def slugify(text: str) -> str:
    """テキストを URL セーフな slug に変換"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def create_medication_knowledge(drug: dict, base_url: str) -> dict:
    """医薬品の FHIR MedicationKnowledge リソースを作成"""
    resource = {
        "resourceType": "MedicationKnowledge",
        "id": drug["slug"],
        "meta": {
            "profile": ["http://hl7.org/fhir/StructureDefinition/MedicationKnowledge"]
        },
        "status": "active",
        "code": {
            "coding": [
                {
                    "system": f"{base_url}/drugs",
                    "code": drug["slug"],
                    "display": drug["name"]
                }
            ],
            "text": drug["name"]
        },
        "intendedJurisdiction": [
            {
                "coding": [
                    {
                        "system": "urn:iso:std:iso:3166",
                        "code": "JP",
                        "display": "Japan"
                    }
                ]
            }
        ],
        "extension": [
            {
                "url": f"{base_url}/fhir/StructureDefinition/evidence-level",
                "valueCode": drug.get("level", "L5")
            }
        ]
    }

    # 元の適応症があれば追加
    if drug.get("original"):
        resource["indicationGuideline"] = [
            {
                "indication": [
                    {
                        "reference": {
                            "display": drug["original"][:200]
                        }
                    }
                ]
            }
        ]

    # ブランド名があれば追加
    if drug.get("brands"):
        resource["synonym"] = drug["brands"]

    return resource


def create_clinical_use_definition(
    drug: dict,
    indication: dict,
    base_url: str
) -> dict:
    """予測適応症の FHIR ClinicalUseDefinition リソースを作成"""
    ind_slug = slugify(indication["name"])
    resource_id = f"{drug['slug']}-{ind_slug}"[:64]

    resource = {
        "resourceType": "ClinicalUseDefinition",
        "id": resource_id,
        "meta": {
            "profile": ["http://hl7.org/fhir/StructureDefinition/ClinicalUseDefinition"]
        },
        "type": "indication",
        "status": {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/publication-status",
                    "code": "draft",
                    "display": "Draft"
                }
            ]
        },
        "subject": [
            {
                "reference": f"MedicationKnowledge/{drug['slug']}"
            }
        ],
        "indication": {
            "diseaseSymptomProcedure": {
                "concept": {
                    "text": indication["name"]
                }
            }
        },
        "extension": [
            {
                "url": f"{base_url}/fhir/StructureDefinition/prediction-status",
                "valueCode": "predicted"
            },
            {
                "url": f"{base_url}/fhir/StructureDefinition/evidence-level",
                "valueCode": indication.get("level", "L5")
            },
            {
                "url": f"{base_url}/fhir/StructureDefinition/txgnn-score",
                "valueDecimal": indication.get("score", 0) / 100
            }
        ]
    }

    return resource


def create_capability_statement(base_url: str, drug_count: int, indication_count: int) -> dict:
    """FHIR CapabilityStatement (metadata) を作成"""
    return {
        "resourceType": "CapabilityStatement",
        "id": "jptxgnn-fhir-server",
        "url": f"{base_url}/fhir/metadata",
        "version": "1.0.0",
        "name": "JpTxGNNFHIRServer",
        "title": "JpTxGNN FHIR Server",
        "status": "active",
        "experimental": True,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "publisher": "JpTxGNN",
        "contact": [
            {
                "telecom": [
                    {
                        "system": "url",
                        "value": base_url
                    }
                ]
            }
        ],
        "description": f"JpTxGNN 医薬品リポジショニング予測データを FHIR リソースとして公開。{drug_count} 医薬品、{indication_count} 予測適応症を含む。",
        "kind": "instance",
        "software": {
            "name": "JpTxGNN Static FHIR API",
            "version": "1.0.0"
        },
        "implementation": {
            "description": "GitHub Pages から提供される静的 FHIR リソース",
            "url": f"{base_url}/fhir"
        },
        "fhirVersion": "4.0.1",
        "format": ["application/fhir+json"],
        "rest": [
            {
                "mode": "server",
                "documentation": "静的 FHIR API - 医薬品リポジショニング予測への読み取り専用アクセス",
                "resource": [
                    {
                        "type": "MedicationKnowledge",
                        "profile": "http://hl7.org/fhir/StructureDefinition/MedicationKnowledge",
                        "interaction": [
                            {"code": "read"}
                        ],
                        "searchParam": [
                            {
                                "name": "_id",
                                "type": "token",
                                "documentation": "医薬品識別子 (slug)"
                            }
                        ]
                    },
                    {
                        "type": "ClinicalUseDefinition",
                        "profile": "http://hl7.org/fhir/StructureDefinition/ClinicalUseDefinition",
                        "interaction": [
                            {"code": "read"}
                        ],
                        "searchParam": [
                            {
                                "name": "subject",
                                "type": "reference",
                                "documentation": "MedicationKnowledge への参照"
                            }
                        ]
                    }
                ]
            }
        ]
    }


def create_bundle(entries: list, base_url: str) -> dict:
    """全リソースを含む FHIR Bundle を作成"""
    return {
        "resourceType": "Bundle",
        "id": "all-predictions",
        "type": "collection",
        "timestamp": datetime.now().isoformat(),
        "total": len(entries),
        "link": [
            {
                "relation": "self",
                "url": f"{base_url}/fhir/Bundle/all-predictions.json"
            }
        ],
        "entry": [
            {
                "fullUrl": f"{base_url}/fhir/{entry['resourceType']}/{entry['id']}",
                "resource": entry
            }
            for entry in entries
        ]
    }


def main():
    """メイン関数：FHIR リソースを生成"""
    # 設定
    base_url = "https://jptxgnn.yao.care"
    project_root = Path(__file__).parent.parent
    input_file = project_root / "docs" / "data" / "search-index.json"
    output_dir = project_root / "docs" / "fhir"

    print(f"検索インデックスを読み込み: {input_file}")

    # 検索インデックスが存在しない場合
    if not input_file.exists():
        print(f"検索インデックスが見つかりません: {input_file}")
        print("先に予測を実行してください: uv run python scripts/run_kg_prediction.py")

        # 空のディレクトリ構造と metadata だけ作成
        (output_dir / "MedicationKnowledge").mkdir(parents=True, exist_ok=True)
        (output_dir / "ClinicalUseDefinition").mkdir(parents=True, exist_ok=True)
        (output_dir / "Bundle").mkdir(parents=True, exist_ok=True)

        capability = create_capability_statement(base_url, 0, 0)
        with open(output_dir / "metadata", "w", encoding="utf-8") as f:
            json.dump(capability, f, ensure_ascii=False, indent=2)
        print("空の CapabilityStatement を生成しました")
        return

    # 検索インデックスを読み込み
    with open(input_file, "r", encoding="utf-8") as f:
        search_index = json.load(f)

    drugs = search_index.get("drugs", [])
    print(f"{len(drugs)} 医薬品を検出")

    # 出力ディレクトリを作成
    (output_dir / "MedicationKnowledge").mkdir(parents=True, exist_ok=True)
    (output_dir / "ClinicalUseDefinition").mkdir(parents=True, exist_ok=True)
    (output_dir / "Bundle").mkdir(parents=True, exist_ok=True)

    # リソースを生成
    all_resources = []
    total_indications = 0

    for drug in drugs:
        # MedicationKnowledge を作成
        med_knowledge = create_medication_knowledge(drug, base_url)
        all_resources.append(med_knowledge)

        # MedicationKnowledge を保存
        output_file = output_dir / "MedicationKnowledge" / f"{drug['slug']}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(med_knowledge, f, ensure_ascii=False, indent=2)

        # 各適応症の ClinicalUseDefinition を作成
        for indication in drug.get("indications", []):
            clinical_use = create_clinical_use_definition(drug, indication, base_url)
            all_resources.append(clinical_use)
            total_indications += 1

            # ClinicalUseDefinition を保存
            output_file = output_dir / "ClinicalUseDefinition" / f"{clinical_use['id']}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(clinical_use, f, ensure_ascii=False, indent=2)

    print(f"{len(drugs)} MedicationKnowledge リソースを生成")
    print(f"{total_indications} ClinicalUseDefinition リソースを生成")

    # CapabilityStatement (metadata) を作成
    capability = create_capability_statement(base_url, len(drugs), total_indications)
    with open(output_dir / "metadata", "w", encoding="utf-8") as f:
        json.dump(capability, f, ensure_ascii=False, indent=2)
    print("CapabilityStatement (metadata) を生成")

    # 全リソースを含む Bundle を作成
    bundle = create_bundle(all_resources, base_url)
    with open(output_dir / "Bundle" / "all-predictions.json", "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print(f"{len(all_resources)} リソースを含む Bundle を生成")

    print(f"\nFHIR リソースの生成完了: {output_dir}")


if __name__ == "__main__":
    main()
