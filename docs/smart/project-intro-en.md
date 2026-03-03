---
layout: default
title: Project Introduction (English)
parent: SMART on FHIR
nav_order: 7
description: JpTxGNN Project Introduction - Drug Repurposing Predictions for Japanese Medicines
permalink: /smart/project-intro-en/
---

# JpTxGNN: Drug Repurposing Predictions for Japanese Medicines

## Overview

JpTxGNN is a drug repurposing prediction platform for Japanese medicines, based on Harvard's TxGNN deep learning model. The system predicts potential new indications for approved medications using knowledge graph and deep learning approaches.

---

## Key Features

### Dual Prediction Methods

| Method | Description | Speed | Accuracy |
|--------|-------------|-------|----------|
| **Knowledge Graph (KG)** | Query existing drug-disease relationships in TxGNN knowledge graph | Fast (minutes) | Medium |
| **Deep Learning (DL)** | Neural network model prediction with confidence scores | Slow (hours) | High |

### Japanese Medicine Focus

- **SSK Medical Drugs**: 19,317 prescription medicines from Japan
- **KEGG DRUG Integration**: Therapeutic classification and indication information
- **DrugBank Mapping**: International drug identifier standardization

### FHIR R4 Compliant API

- **MedicationKnowledge**: Drug information resources
- **ClinicalUseDefinition**: Predicted indication resources
- **Bundle**: Collection of all predictions

---

## Statistics

| Metric | Value |
|--------|-------|
| Total Drugs | 3,824 |
| DrugBank Mappings | 142 |
| KG Predictions | 33,901 |
| DL Predictions | 2,419,822 |
| Integrated Predictions (≥90%) | 155,638 |

---

## Prediction Workflow

1. **Data Collection**: Integrate SSK medicines + KEGG therapeutic information
2. **DrugBank Mapping**: Map ingredient names to DrugBank IDs
3. **KG Prediction**: Extract known relationships from TxGNN knowledge graph
4. **DL Prediction**: Predict new relationships using deep learning model
5. **Integration & Filtering**: Extract predictions with confidence ≥90%

---

## TxGNN Score Interpretation

The TxGNN score represents model confidence for drug-disease pairs, ranging from 0 to 1.

| Threshold | Meaning | Recommended Use |
|-----------|---------|-----------------|
| ≥ 0.99 | Very high confidence | Priority verification |
| ≥ 0.90 | High confidence | Detailed investigation |
| ≥ 0.50 | Medium confidence | Reference information |
| < 0.50 | Low confidence | Additional validation needed |

---

## Technical Stack

- **Backend**: Python, pandas, PyTorch, DGL
- **Frontend**: Jekyll, JavaScript, Fuse.js
- **API**: HL7 FHIR R4
- **Hosting**: GitHub Pages

---

## Data Sources

| Data | Source | Description |
|------|--------|-------------|
| Medicines | Japan SSK | 19,317 prescription medicines |
| Therapeutic Info | KEGG DRUG | Indications and effects |
| Knowledge Graph | Harvard TxGNN | 17,080 diseases, 7,957 drugs |

---

## Disclaimer

This project is for **research purposes only** and does not constitute medical advice. Drug repurposing candidates require clinical validation before application.

---

## Citation

If you use this dataset or software, please cite:

```bibtex
@software{jptxgnn2026,
  author       = {Yao.Care},
  title        = {JpTxGNN: Drug Repurposing Predictions for Japanese Medicines},
  year         = 2026,
  url          = {https://github.com/yao-care/JpTxGNN}
}
```

Also cite the original TxGNN paper:

```bibtex
@article{huang2024txgnn,
  title={A foundation model for clinician-centered drug repurposing},
  author={Huang, Kexin and Chandak, Payal and Wang, Qianwen and Haber, Shreyas and Zitnik, Marinka},
  journal={Nature Medicine},
  year={2024},
  doi={10.1038/s41591-024-03233-x}
}
```

---

## Links

- [Website](https://jptxgnn.yao.care)
- [GitHub Repository](https://github.com/yao-care/JpTxGNN)
- [TxGNN Paper](https://www.nature.com/articles/s41591-024-03233-x)
- [TxGNN Explorer](http://txgnn.org)
