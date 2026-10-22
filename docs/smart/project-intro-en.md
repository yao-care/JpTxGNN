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

JpTxGNN is a drug repurposing prediction platform for Japanese medicines, based on Harvard's TxGNN deep learning model. The system predicts potential new indications for approved medications with the TxGNN deep learning model, after excluding uses already recorded in the knowledge graph.

---

## Key Features

### Prediction Method

| Step | Description |
|------|-------------|
| **Deep Learning (DL)** | TxGNN neural network scores each drug–disease pair; drug pages list scores ≥ 0.99 |
| **Known-use check (KG)** | Drug–disease relationships already recorded in the TxGNN knowledge graph are excluded; they are known uses, not predictions |

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
| Total Drugs | {{ site.data.site_stats.drugs }} |
| DrugBank Mappings | 142 |
| KG Known Uses (excluded) | 33,901 |
| DL Scored Pairs | 2,419,822 |
| Predicted New Indications (known uses excluded) | {{ site.data.site_stats.indications }} |

---

## Prediction Workflow

1. **Data Collection**: Integrate SSK medicines + KEGG therapeutic information
2. **DrugBank Mapping**: Map ingredient names to DrugBank IDs
3. **Known-use check (KG)**: Exclude relationships already recorded in the TxGNN knowledge graph
4. **DL Prediction**: Predict new relationships using deep learning model
5. **Integration & Filtering**: Keep predictions with score ≥0.99 (top 10 per drug)

---

## TxGNN Score Interpretation

The TxGNN score (0 to 1) ranks drug-disease pairs inside the model; it is not a probability of clinical efficacy.

The site only lists predictions with a score of 0.99 or higher, up to the top 10 per drug, after known uses are excluded.

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
