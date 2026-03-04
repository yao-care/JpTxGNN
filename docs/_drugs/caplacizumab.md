---
layout: default
title: Caplacizumab
parent: 僅模型預測 (L5)
nav_order: 37
evidence_level: L5
indication_count: 1
---

# Caplacizumab
{: .fs-9 }

證據等級: **L5** | 預測適應症: **1** 個
{: .fs-6 .fw-300 }

---

## 目錄
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 藥師評估報告

</div>

# Caplacizumab：從後天性TTP到血小板原發釋放障礙

## 一句話總結
Caplacizumab 原為治療後天性血栓性血小板低下紫斑症(aTTP)的抗von Willebrand因子奈米抗體，TxGNN 預測其可能對血小板原發釋放障礙(primary release disorder of platelets)有治療潛力。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 後天性血栓性血小板低下紫斑症 (aTTP)，合併血漿置換術及免疫抑制劑使用 |
| 預測新適應症 | 血小板原發釋放障礙 (primary release disorder of platelets) |
| TxGNN 預測分數 | 99.9998% |
| 證據等級 | L5 (僅預測) |
| 台灣上市 | 已上市 |
| 許可證數 | 1張 (多個包裝規格) |
| 建議決策 | Hold |

## 為什麼這個預測合理？
Caplacizumab 是一種人源化雙價奈米抗體(Nanobody)：

1. **作用機轉**：結合 von Willebrand 因子(vWF)的A1區域，阻斷血小板與vWF的交互作用
2. **抗血栓形成**：防止血小板在vWF多聚體上的異常聚集
3. **高預測分數**：TxGNN 給予極高分數(99.9998%)，排名第8

然而，需謹慎看待此預測：
- 血小板原發釋放障礙是血小板功能缺陷疾病，涉及血小板釋放反應異常
- Caplacizumab 作用於 vWF-血小板軸，而非直接影響血小板釋放機制
- 理論上 caplacizumab 可能加重而非改善血小板功能障礙

## 臨床試驗證據
目前無針對 caplacizumab 治療血小板原發釋放障礙的臨床試驗。

**與原適應症(aTTP)相關的重要臨床試驗**：

1. **HERCULES 試驗 (NCT02553317)** - Phase III
   - 145位患者參與
   - 證實 caplacizumab 可顯著縮短血小板恢復時間
   - 減少 aTTP 復發及相關死亡

2. **Post-HERCULES (NCT02878603)** - 長期追蹤
   - 評估 caplacizumab 的長期安全性
   - 104位患者完成追蹤

3. **日本 Phase 2/3 試驗 (NCT04074187)**
   - 21位日本患者
   - 確認在亞洲族群的療效與安全性

## 文獻證據
關於原適應症(aTTP)的重要文獻：

1. **Scully M 等人 (2019)** - *New England Journal of Medicine*
   - HERCULES 試驗結果發表
   - 確立 caplacizumab 在 aTTP 治療中的地位

2. **Peyvandi F 等人 (2016)** - *New England Journal of Medicine*
   - Phase II 試驗首次證實 caplacizumab 的療效

3. **Zheng XL 等人 (2020)** - *Journal of Thrombosis and Haemostasis*
   - ISTH 治療 TTP 指引
   - 納入 caplacizumab 作為標準治療選項

無針對血小板原發釋放障礙的相關文獻。

## 台灣上市資訊

| 許可證字號 | 商品名 | 劑型 | 許可證持有者 |
|-----------|--------|------|-------------|
| 衛部菌疫輸字第001243號 | 可利康凍晶注射劑10毫克 (Cablivi) | 注射劑 | 賽諾菲股份有限公司 |

核准適應症：
- 適用於合併血漿置換術及免疫抑制劑，治療後天性血栓性血小板低下紫斑症(aTTP)
- 適用族群：成人及12歲以上且體重40公斤以上的青少年

## 安全性考量
### 常見副作用
- 出血事件(鼻出血、牙齦出血最常見)
- 頭痛
- 蕁麻疹

### 嚴重警語
- 出血風險增加
- 使用期間應避免手術及侵入性處置
- 需監測出血徵象

### 藥物交互作用(主要)

| 交互作用藥物 | 嚴重程度 |
|-------------|---------|
| 阿斯匹靈 | 重度 |
| 抗凝血劑(apixaban, rivaroxaban等) | 重度 |
| 血小板抑制劑 | 重度 |
| Fondaparinux | 重度 |
| NSAIDs | 中度 |

## 結論與下一步
**證據等級**：L5 (僅 TxGNN 預測，無臨床或藥理學支持)

**建議**：Hold (暫不建議)
1. 血小板原發釋放障礙與 caplacizumab 的作用機轉無明顯關聯
2. 抑制 vWF-血小板交互作用理論上可能惡化而非改善血小板釋放功能
3. 極高的 TxGNN 分數可能反映兩者在血小板相關疾病知識圖譜中的位置接近，而非真正的治療關聯

**下一步建議**：
- 不建議進行臨床探索
- 若臨床遇到 aTTP 合併血小板功能障礙的病例，可收集相關數據以釐清
- 建議專注於 caplacizumab 在其他血栓性微血管病變(如非典型HUS)的潛在應用研究

**特別注意**：此預測可能為 TxGNN 演算法的偽陽性結果，臨床上不應依據此預測進行治療決策。


---

