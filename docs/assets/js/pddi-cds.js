/**
 * JpTxGNN PDDI-CDS (Potential Drug-Drug Interaction Clinical Decision Support)
 *
 * Implements HL7 PDDI-CDS Implementation Guide patterns for
 * contextualized drug-drug interaction alerts.
 *
 * Reference: https://github.com/HL7/PDDI-CDS
 *
 * @author JpTxGNN Team
 * @version 1.0.0
 */
(function(global) {
  'use strict';

  /**
   * PDDI Severity Levels per HL7 PDDI-CDS IG
   */
  const PDDI_INDICATOR = {
    CRITICAL: 'critical',   // Immediate attention required
    WARNING: 'warning',     // Attention needed
    INFO: 'info'           // Informational
  };

  /**
   * PDDI Alert Types
   */
  const ALERT_TYPE = {
    CONTRAINDICATED: 'contraindicated',
    CONDITIONAL: 'conditional',
    RELATIVE: 'relative'
  };

  /**
   * PDDI Knowledge Base - High-priority interactions with contextual factors
   * Based on DDI-CDS.org research and DDInter 2.0
   */
  const PDDI_KNOWLEDGE_BASE = [
    // Warfarin-NSAID (DDInteract pattern)
    {
      id: 'warfarin-nsaid',
      drugs: {
        object: ['warfarin', 'coumadin'],
        precipitant: ['ibuprofen', 'naproxen', 'aspirin', 'diclofenac', 'celecoxib', 'meloxicam']
      },
      alertType: ALERT_TYPE.CONDITIONAL,
      indicator: PDDI_INDICATOR.WARNING,
      clinicalConsequence: '增加胃腸道出血和全身出血風險',
      frequency: '常見（約 10-15% 使用者會有臨床顯著出血）',
      mechanism: 'NSAIDs 抑制血小板功能並可能增加 Warfarin 的抗凝效果',
      contextualFactors: [
        {
          factor: 'GI 出血病史',
          impact: '風險顯著增加',
          recommendation: '強烈建議避免併用'
        },
        {
          factor: '年齡 > 65 歲',
          impact: '風險增加',
          recommendation: '若必須使用，加上 PPI 保護'
        },
        {
          factor: '使用 PPI/H2 blocker',
          impact: '風險降低',
          recommendation: '可考慮短期使用'
        },
        {
          factor: 'INR 控制不穩定',
          impact: '風險增加',
          recommendation: '避免併用'
        }
      ],
      managementOptions: [
        {
          option: '使用 Acetaminophen 替代',
          description: '對於疼痛管理，Acetaminophen 是較安全的選擇',
          recommended: true
        },
        {
          option: '加上 PPI',
          description: '若必須使用 NSAID，加上 PPI（如 Omeprazole）降低 GI 出血風險',
          recommended: true
        },
        {
          option: '選用 COX-2 抑制劑',
          description: 'Celecoxib 相對 GI 風險較低，但仍需謹慎',
          recommended: false
        },
        {
          option: '短期使用 + 密切監測',
          description: '使用最低有效劑量，最短時間，並監測出血徵兆',
          recommended: false
        }
      ],
      evidence: {
        level: 'High',
        sources: ['DDInteract RCT', 'AHRQ Evidence Review', 'DDInter 2.0']
      }
    },

    // Colchicine-CYP3A4 Inhibitor
    {
      id: 'colchicine-cyp3a4',
      drugs: {
        object: ['colchicine', 'colcrys'],
        precipitant: ['clarithromycin', 'erythromycin', 'ritonavir', 'cobicistat', 'itraconazole', 'ketoconazole']
      },
      alertType: ALERT_TYPE.CONTRAINDICATED,
      indicator: PDDI_INDICATOR.CRITICAL,
      clinicalConsequence: '嚴重 Colchicine 毒性（骨髓抑制、神經病變、多重器官衰竭）',
      frequency: '罕見但潛在致命',
      mechanism: 'CYP3A4 抑制劑大幅增加 Colchicine 血中濃度（可達 2-4 倍）',
      contextualFactors: [
        {
          factor: '腎功能不全',
          impact: '禁止併用',
          recommendation: '絕對禁忌'
        },
        {
          factor: '肝功能不全',
          impact: '禁止併用',
          recommendation: '絕對禁忌'
        },
        {
          factor: '正常腎肝功能',
          impact: '風險仍高',
          recommendation: '顯著降低 Colchicine 劑量或避免'
        }
      ],
      managementOptions: [
        {
          option: '避免併用',
          description: '選用替代抗生素或抗黴菌藥',
          recommended: true
        },
        {
          option: '降低 Colchicine 劑量',
          description: '若必須併用，Colchicine 劑量減至 0.3mg 每日或更低',
          recommended: false
        },
        {
          option: '暫停 Colchicine',
          description: '在使用強效 CYP3A4 抑制劑期間暫停 Colchicine',
          recommended: true
        }
      ],
      evidence: {
        level: 'High',
        sources: ['DDI-CDS.org Colchicine CDS', 'FDA Warning', 'DDInter 2.0']
      }
    },

    // Tizanidine-CYP1A2 Inhibitor
    {
      id: 'tizanidine-cyp1a2',
      drugs: {
        object: ['tizanidine', 'zanaflex'],
        precipitant: ['ciprofloxacin', 'fluvoxamine', 'zileuton']
      },
      alertType: ALERT_TYPE.CONTRAINDICATED,
      indicator: PDDI_INDICATOR.CRITICAL,
      clinicalConsequence: '嚴重低血壓、過度鎮靜',
      frequency: '使用 Ciprofloxacin 時 AUC 增加 10 倍',
      mechanism: 'CYP1A2 抑制劑顯著增加 Tizanidine 生體可用率',
      contextualFactors: [
        {
          factor: '使用 Ciprofloxacin',
          impact: '禁止併用',
          recommendation: '改用其他抗生素'
        },
        {
          factor: '使用 Fluvoxamine',
          impact: '禁止併用',
          recommendation: '改用其他 SSRI'
        }
      ],
      managementOptions: [
        {
          option: '避免併用',
          description: '選用不抑制 CYP1A2 的替代藥物',
          recommended: true
        },
        {
          option: '替代肌肉鬆弛劑',
          description: '使用 Baclofen 或 Cyclobenzaprine 替代',
          recommended: true
        }
      ],
      evidence: {
        level: 'High',
        sources: ['DDI-CDS.org Tizanidine CDS', 'FDA Label', 'DDInter 2.0']
      }
    },

    // Digoxin-Amiodarone
    {
      id: 'digoxin-amiodarone',
      drugs: {
        object: ['digoxin', 'lanoxin'],
        precipitant: ['amiodarone', 'cordarone']
      },
      alertType: ALERT_TYPE.CONDITIONAL,
      indicator: PDDI_INDICATOR.WARNING,
      clinicalConsequence: 'Digoxin 毒性（心律不整、噁心嘔吐、視覺障礙）',
      frequency: 'Digoxin 濃度平均增加 70%',
      mechanism: 'Amiodarone 抑制 Digoxin 的腎臟和非腎臟清除',
      contextualFactors: [
        {
          factor: '腎功能不全',
          impact: '風險增加',
          recommendation: '更積極降低 Digoxin 劑量'
        },
        {
          factor: '電解質異常（低血鉀）',
          impact: '風險顯著增加',
          recommendation: '校正電解質並密切監測'
        }
      ],
      managementOptions: [
        {
          option: '降低 Digoxin 劑量 50%',
          description: '開始 Amiodarone 時立即將 Digoxin 劑量減半',
          recommended: true
        },
        {
          option: '監測 Digoxin 濃度',
          description: '定期監測血中濃度，目標 0.5-1.0 ng/mL',
          recommended: true
        },
        {
          option: '監測心電圖',
          description: '注意心動過緩和心律不整',
          recommended: true
        }
      ],
      evidence: {
        level: 'High',
        sources: ['Clinical Pharmacokinetics Studies', 'DDInter 2.0']
      }
    },

    // QT Prolongation (multiple drugs)
    {
      id: 'qt-prolongation-combo',
      drugs: {
        object: ['amiodarone', 'sotalol', 'dofetilide', 'dronedarone'],
        precipitant: ['moxifloxacin', 'haloperidol', 'ziprasidone', 'ondansetron', 'methadone']
      },
      alertType: ALERT_TYPE.CONDITIONAL,
      indicator: PDDI_INDICATOR.CRITICAL,
      clinicalConsequence: 'Torsades de Pointes（多形性心室頻脈）',
      frequency: '罕見但潛在致命',
      mechanism: '多重 QT 延長藥物的加成效應',
      contextualFactors: [
        {
          factor: '電解質異常',
          impact: '風險顯著增加',
          recommendation: '校正低血鉀、低血鎂'
        },
        {
          factor: '基礎 QTc > 450ms',
          impact: '禁止併用',
          recommendation: '避免加用 QT 延長藥物'
        },
        {
          factor: '女性',
          impact: '風險增加',
          recommendation: '更謹慎監測'
        },
        {
          factor: '心臟病史',
          impact: '風險增加',
          recommendation: '考慮替代藥物'
        }
      ],
      managementOptions: [
        {
          option: '避免併用',
          description: '選用不延長 QT 的替代藥物',
          recommended: true
        },
        {
          option: '心電圖監測',
          description: '若必須併用，定期監測 QTc 間期',
          recommended: true
        },
        {
          option: '校正電解質',
          description: '確保血鉀 > 4.0 mEq/L，血鎂 > 2.0 mg/dL',
          recommended: true
        }
      ],
      evidence: {
        level: 'High',
        sources: ['CredibleMeds QT Drug Lists', 'FDA Warnings', 'DDInter 2.0']
      }
    }
  ];

  /**
   * Find matching PDDI for given drugs
   */
  function findPDDI(drug1, drug2) {
    const d1 = drug1.toLowerCase();
    const d2 = drug2.toLowerCase();

    for (const pddi of PDDI_KNOWLEDGE_BASE) {
      const objectMatch = pddi.drugs.object.some(d => d1.includes(d) || d.includes(d1)) ||
                         pddi.drugs.object.some(d => d2.includes(d) || d.includes(d2));
      const precipitantMatch = pddi.drugs.precipitant.some(d => d1.includes(d) || d.includes(d1)) ||
                               pddi.drugs.precipitant.some(d => d2.includes(d) || d.includes(d2));

      if (objectMatch && precipitantMatch) {
        // Determine which is which
        const objectDrug = pddi.drugs.object.some(d => d1.includes(d) || d.includes(d1)) ? drug1 : drug2;
        const precipitantDrug = objectDrug === drug1 ? drug2 : drug1;

        return {
          ...pddi,
          objectDrug,
          precipitantDrug
        };
      }
    }

    return null;
  }

  /**
   * Check all drug pairs for PDDI
   */
  function checkPDDI(medications) {
    if (!medications || medications.length < 2) {
      return [];
    }

    const alerts = [];
    const seen = new Set();

    for (let i = 0; i < medications.length; i++) {
      for (let j = i + 1; j < medications.length; j++) {
        const pairKey = [medications[i], medications[j]].sort().join('|');
        if (seen.has(pairKey)) continue;
        seen.add(pairKey);

        const pddi = findPDDI(medications[i], medications[j]);
        if (pddi) {
          alerts.push(pddi);
        }
      }
    }

    // Sort by severity
    return alerts.sort((a, b) => {
      const priority = { critical: 3, warning: 2, info: 1 };
      return priority[b.indicator] - priority[a.indicator];
    });
  }

  /**
   * Generate CDS Hooks card for a PDDI alert
   * Following HL7 PDDI-CDS IG structure
   */
  function generateCDSHooksCard(pddi) {
    const card = {
      uuid: `pddi-${pddi.id}-${Date.now()}`,
      summary: `${pddi.objectDrug} + ${pddi.precipitantDrug}: ${pddi.clinicalConsequence}`,
      indicator: pddi.indicator,
      detail: generateDetailMarkdown(pddi),
      source: {
        label: 'JpTxGNN PDDI-CDS',
        url: 'https://jptxgnn.yao.care/smart/',
        icon: 'https://jptxgnn.yao.care/assets/img/icon-192.png'
      },
      suggestions: pddi.managementOptions
        .filter(opt => opt.recommended)
        .map((opt, idx) => ({
          label: opt.option,
          uuid: `suggestion-${pddi.id}-${idx}`,
          actions: []
        })),
      links: [
        {
          label: '查看完整資訊',
          url: `https://jptxgnn.yao.care/drugs/`,
          type: 'absolute'
        }
      ],
      overrideReasons: [
        { code: 'patient-aware', display: '病患已知悉風險' },
        { code: 'benefit-outweighs', display: '效益大於風險' },
        { code: 'alternative-unavailable', display: '無可用替代方案' },
        { code: 'monitoring-in-place', display: '已有監測計畫' }
      ]
    };

    return card;
  }

  /**
   * Generate detailed markdown for PDDI alert
   */
  function generateDetailMarkdown(pddi) {
    let md = `## 藥物交互作用警示\n\n`;
    md += `**交互作用類型**: ${getAlertTypeLabel(pddi.alertType)}\n\n`;
    md += `**機轉**: ${pddi.mechanism}\n\n`;
    md += `**臨床後果**: ${pddi.clinicalConsequence}\n\n`;
    md += `**發生頻率**: ${pddi.frequency}\n\n`;

    md += `### 情境因素\n\n`;
    pddi.contextualFactors.forEach(cf => {
      md += `- **${cf.factor}**: ${cf.impact} - ${cf.recommendation}\n`;
    });

    md += `\n### 處置選項\n\n`;
    pddi.managementOptions.forEach(opt => {
      const marker = opt.recommended ? '✓' : '○';
      md += `- ${marker} **${opt.option}**: ${opt.description}\n`;
    });

    md += `\n### 證據等級\n\n`;
    md += `等級: ${pddi.evidence.level}\n`;
    md += `來源: ${pddi.evidence.sources.join(', ')}\n`;

    return md;
  }

  /**
   * Get human-readable alert type label
   */
  function getAlertTypeLabel(type) {
    const labels = {
      contraindicated: '禁止併用',
      conditional: '條件性警示',
      relative: '相對禁忌'
    };
    return labels[type] || type;
  }

  /**
   * Render PDDI alert as HTML
   */
  function renderPDDIAlert(pddi) {
    const indicatorClass = {
      critical: 'pddi-critical',
      warning: 'pddi-warning',
      info: 'pddi-info'
    }[pddi.indicator] || 'pddi-info';

    let html = `
      <div class="pddi-alert ${indicatorClass}">
        <div class="pddi-header">
          <span class="pddi-indicator">${getIndicatorLabel(pddi.indicator)}</span>
          <span class="pddi-type">${getAlertTypeLabel(pddi.alertType)}</span>
        </div>
        <div class="pddi-drugs">
          <strong>${escapeHtml(pddi.objectDrug)}</strong> +
          <strong>${escapeHtml(pddi.precipitantDrug)}</strong>
        </div>
        <div class="pddi-consequence">${escapeHtml(pddi.clinicalConsequence)}</div>
        <div class="pddi-mechanism">
          <strong>機轉：</strong>${escapeHtml(pddi.mechanism)}
        </div>
        <div class="pddi-context">
          <strong>情境因素：</strong>
          <ul>
    `;

    pddi.contextualFactors.forEach(cf => {
      html += `<li><strong>${escapeHtml(cf.factor)}：</strong>${escapeHtml(cf.impact)} - ${escapeHtml(cf.recommendation)}</li>`;
    });

    html += `
          </ul>
        </div>
        <div class="pddi-management">
          <strong>處置建議：</strong>
          <ul>
    `;

    pddi.managementOptions.forEach(opt => {
      const marker = opt.recommended ? '✓' : '○';
      html += `<li class="${opt.recommended ? 'recommended' : ''}">${marker} <strong>${escapeHtml(opt.option)}：</strong>${escapeHtml(opt.description)}</li>`;
    });

    html += `
          </ul>
        </div>
        <div class="pddi-evidence">
          <strong>證據等級：</strong>${pddi.evidence.level} |
          <strong>來源：</strong>${pddi.evidence.sources.join(', ')}
        </div>
      </div>
    `;

    return html;
  }

  function getIndicatorLabel(indicator) {
    const labels = {
      critical: '⚠️ 嚴重',
      warning: '⚡ 警告',
      info: 'ℹ️ 資訊'
    };
    return labels[indicator] || indicator;
  }

  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Export
  global.JpTxGNN = global.JpTxGNN || {};
  global.JpTxGNN.PDDI = {
    checkPDDI: checkPDDI,
    findPDDI: findPDDI,
    generateCDSHooksCard: generateCDSHooksCard,
    renderPDDIAlert: renderPDDIAlert,
    INDICATOR: PDDI_INDICATOR,
    ALERT_TYPE: ALERT_TYPE,
    KNOWLEDGE_BASE: PDDI_KNOWLEDGE_BASE
  };

})(typeof window !== 'undefined' ? window : this);
