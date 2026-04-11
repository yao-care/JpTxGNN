/**
 * JpTxGNN Drug-Drug Interaction Checker
 *
 * Client-side DDI checking based on DDInter 2.0 database.
 * Provides real-time interaction alerts for drug repurposing candidates.
 *
 * @author JpTxGNN Team
 * @version 1.0.0
 */
(function(global) {
  'use strict';

  const CONFIG = {
    ddiDataUrl: '/data/ddi-index.json',
    maxAlerts: 10
  };

  // Severity levels with priority (higher = more severe)
  const SEVERITY = {
    'Major': { priority: 3, class: 'ddi-major', label: '重度' },
    'Moderate': { priority: 2, class: 'ddi-moderate', label: '中度' },
    'Minor': { priority: 1, class: 'ddi-minor', label: '輕度' }
  };

  // High-priority DDI rules (curated from DDInter 2.0)
  // Format: { drug1: [synonym list], drug2: [synonym list], severity, summary, detail }
  const CURATED_DDI_RULES = [
    {
      drugs: [
        ['warfarin', 'coumadin'],
        ['ibuprofen', 'advil', 'motrin', 'brufen']
      ],
      severity: 'Major',
      summary: 'Warfarin + Ibuprofen: 出血風險增加',
      detail: 'NSAIDs 會抑制血小板功能並可能增加 Warfarin 的抗凝效果，顯著增加胃腸道出血風險。',
      recommendation: '建議使用 Acetaminophen 替代，或加上 PPI 胃保護。'
    },
    {
      drugs: [
        ['warfarin', 'coumadin'],
        ['aspirin', 'acetylsalicylic acid']
      ],
      severity: 'Major',
      summary: 'Warfarin + Aspirin: 出血風險增加',
      detail: '兩者皆影響凝血功能，併用會大幅增加出血風險。',
      recommendation: '若必須併用，應使用低劑量 Aspirin 並密切監測 INR。'
    },
    {
      drugs: [
        ['warfarin', 'coumadin'],
        ['naproxen', 'aleve', 'naprosyn']
      ],
      severity: 'Major',
      summary: 'Warfarin + Naproxen: 出血風險增加',
      detail: 'Naproxen 與 Warfarin 併用會增加胃腸道出血和其他出血事件的風險。',
      recommendation: '建議使用 Acetaminophen 替代止痛。'
    },
    {
      drugs: [
        ['metformin', 'glucophage'],
        ['iodixanol', 'visipaque', 'iopamidol', 'isovue', 'contrast']
      ],
      severity: 'Major',
      summary: 'Metformin + 含碘顯影劑: 乳酸中毒風險',
      detail: '顯影劑可能導致急性腎損傷，使 Metformin 蓄積而引起乳酸中毒。',
      recommendation: '檢查前 48 小時停用 Metformin，確認腎功能正常後再恢復。'
    },
    {
      drugs: [
        ['colchicine', 'colcrys'],
        ['clarithromycin', 'biaxin', 'klacid']
      ],
      severity: 'Major',
      summary: 'Colchicine + Clarithromycin: 毒性風險',
      detail: 'Clarithromycin 是強效 CYP3A4 抑制劑，會大幅增加 Colchicine 血中濃度。',
      recommendation: '避免併用或顯著降低 Colchicine 劑量。'
    },
    {
      drugs: [
        ['colchicine', 'colcrys'],
        ['ritonavir', 'norvir', 'cobicistat', 'tybost']
      ],
      severity: 'Major',
      summary: 'Colchicine + HIV 蛋白酶抑制劑: 嚴重毒性風險',
      detail: 'HIV 蛋白酶抑制劑會極大增加 Colchicine 濃度，可能導致致命性毒性。',
      recommendation: '腎/肝功能不全患者禁止併用。'
    },
    {
      drugs: [
        ['simvastatin', 'zocor'],
        ['amiodarone', 'cordarone']
      ],
      severity: 'Major',
      summary: 'Simvastatin + Amiodarone: 肌肉病變風險',
      detail: 'Amiodarone 會增加 Simvastatin 濃度，增加橫紋肌溶解症風險。',
      recommendation: 'Simvastatin 劑量不應超過 20mg/天，或改用其他 Statin。'
    },
    {
      drugs: [
        ['fluoxetine', 'prozac', 'sertraline', 'zoloft', 'paroxetine', 'paxil'],
        ['tramadol', 'ultram']
      ],
      severity: 'Major',
      summary: 'SSRI + Tramadol: 血清素症候群風險',
      detail: '兩者皆增加血清素活性，併用可能引起危及生命的血清素症候群。',
      recommendation: '密切監測症狀（高熱、肌躍、意識改變），考慮替代止痛藥。'
    },
    {
      drugs: [
        ['fluoxetine', 'prozac', 'sertraline', 'zoloft', 'paroxetine', 'paxil'],
        ['linezolid', 'zyvox']
      ],
      severity: 'Major',
      summary: 'SSRI + Linezolid: 血清素症候群風險',
      detail: 'Linezolid 是 MAO 抑制劑，與 SSRI 併用高度危險。',
      recommendation: '避免併用。若必須使用 Linezolid，應停用 SSRI 並等待適當清除期。'
    },
    {
      drugs: [
        ['amiodarone', 'cordarone'],
        ['moxifloxacin', 'avelox']
      ],
      severity: 'Major',
      summary: 'Amiodarone + Moxifloxacin: QT 延長風險',
      detail: '兩者皆可延長 QT 間期，併用會增加 Torsades de Pointes 風險。',
      recommendation: '避免併用或密切監測心電圖。'
    },
    {
      drugs: [
        ['digoxin', 'lanoxin'],
        ['amiodarone', 'cordarone']
      ],
      severity: 'Major',
      summary: 'Digoxin + Amiodarone: Digoxin 毒性風險',
      detail: 'Amiodarone 會增加 Digoxin 血中濃度約 70%。',
      recommendation: '開始 Amiodarone 時，將 Digoxin 劑量減半並監測血中濃度。'
    },
    {
      drugs: [
        ['clopidogrel', 'plavix'],
        ['omeprazole', 'prilosec', 'esomeprazole', 'nexium']
      ],
      severity: 'Moderate',
      summary: 'Clopidogrel + PPI: 抗血小板效果降低',
      detail: 'Omeprazole 會抑制 CYP2C19，降低 Clopidogrel 轉化為活性代謝物。',
      recommendation: '考慮使用 Pantoprazole 或 H2 blocker 替代。'
    },
    {
      drugs: [
        ['lithium', 'lithobid'],
        ['ibuprofen', 'advil', 'naproxen', 'aleve', 'diclofenac']
      ],
      severity: 'Major',
      summary: 'Lithium + NSAIDs: Lithium 毒性風險',
      detail: 'NSAIDs 會減少 Lithium 腎臟排除，導致血中濃度升高。',
      recommendation: '避免併用或密切監測 Lithium 濃度。'
    },
    {
      drugs: [
        ['potassium', 'k-dur', 'klor-con'],
        ['spironolactone', 'aldactone', 'eplerenone', 'inspra']
      ],
      severity: 'Major',
      summary: '鉀補充劑 + 保鉀利尿劑: 高血鉀風險',
      detail: '兩者皆增加血鉀，併用可能導致危及生命的高血鉀症。',
      recommendation: '定期監測血鉀，避免同時補充鉀。'
    },
    {
      drugs: [
        ['methotrexate', 'trexall'],
        ['trimethoprim', 'bactrim', 'septra', 'sulfamethoxazole']
      ],
      severity: 'Major',
      summary: 'Methotrexate + TMP-SMX: 骨髓抑制風險',
      detail: '兩者皆抑制葉酸代謝，併用會增加骨髓抑制和黏膜炎風險。',
      recommendation: '避免併用或確保充足葉酸補充並密切監測血球。'
    }
  ];

  let ddiIndex = null;
  let isLoaded = false;

  /**
   * Load DDI index data
   */
  async function loadDDIIndex() {
    if (isLoaded) return;

    try {
      const response = await fetch(CONFIG.ddiDataUrl);
      if (response.ok) {
        ddiIndex = await response.json();
        isLoaded = true;
        console.log('DDI index loaded:', ddiIndex?.count || 0, 'interactions');
      }
    } catch (error) {
      console.warn('DDI index not available, using curated rules only');
      isLoaded = true;
    }
  }

  /**
   * Normalize drug name for comparison
   */
  function normalizeDrugName(name) {
    if (!name) return '';
    return name.toLowerCase()
      .replace(/\s+/g, ' ')
      .replace(/[^a-z0-9\s]/g, '')
      .trim();
  }

  /**
   * Check if a drug name matches any of the synonyms
   */
  function matchesDrug(drugName, synonyms) {
    const normalized = normalizeDrugName(drugName);
    return synonyms.some(syn => {
      const normalizedSyn = normalizeDrugName(syn);
      return normalized.includes(normalizedSyn) || normalizedSyn.includes(normalized);
    });
  }

  /**
   * Check for DDI between two drugs using curated rules
   */
  function checkCuratedDDI(drug1, drug2) {
    const alerts = [];

    for (const rule of CURATED_DDI_RULES) {
      const [drugGroup1, drugGroup2] = rule.drugs;

      // Check if drug1 matches group1 and drug2 matches group2, or vice versa
      if (
        (matchesDrug(drug1, drugGroup1) && matchesDrug(drug2, drugGroup2)) ||
        (matchesDrug(drug1, drugGroup2) && matchesDrug(drug2, drugGroup1))
      ) {
        alerts.push({
          drug1: drug1,
          drug2: drug2,
          severity: rule.severity,
          severityInfo: SEVERITY[rule.severity],
          summary: rule.summary,
          detail: rule.detail,
          recommendation: rule.recommendation,
          source: 'JpTxGNN DDI Rules (based on DDInter 2.0)'
        });
      }
    }

    return alerts;
  }

  /**
   * Check DDI for a list of medications
   * @param {string[]} medications - Array of medication names
   * @returns {Object[]} Array of DDI alerts
   */
  function checkInteractions(medications) {
    if (!medications || medications.length < 2) {
      return [];
    }

    const allAlerts = [];
    const seen = new Set();

    // Check all pairs
    for (let i = 0; i < medications.length; i++) {
      for (let j = i + 1; j < medications.length; j++) {
        const drug1 = medications[i];
        const drug2 = medications[j];
        const pairKey = [drug1, drug2].sort().join('|');

        if (seen.has(pairKey)) continue;
        seen.add(pairKey);

        const alerts = checkCuratedDDI(drug1, drug2);
        allAlerts.push(...alerts);
      }
    }

    // Sort by severity (highest first) and limit
    return allAlerts
      .sort((a, b) => b.severityInfo.priority - a.severityInfo.priority)
      .slice(0, CONFIG.maxAlerts);
  }

  /**
   * Check if a new drug has interactions with existing medications
   * @param {string} newDrug - The new drug to check
   * @param {string[]} currentMeds - Array of current medication names
   * @returns {Object[]} Array of DDI alerts
   */
  function checkNewDrug(newDrug, currentMeds) {
    if (!newDrug || !currentMeds || currentMeds.length === 0) {
      return [];
    }

    const allAlerts = [];

    for (const currentDrug of currentMeds) {
      const alerts = checkCuratedDDI(newDrug, currentDrug);
      allAlerts.push(...alerts);
    }

    return allAlerts
      .sort((a, b) => b.severityInfo.priority - a.severityInfo.priority);
  }

  /**
   * Format alerts as HTML for display
   */
  function formatAlertsHTML(alerts) {
    if (!alerts || alerts.length === 0) {
      return '<div class="ddi-no-alerts">未發現藥物交互作用警示</div>';
    }

    let html = '<div class="ddi-alerts">';

    alerts.forEach((alert, index) => {
      html += `
        <div class="ddi-alert ${alert.severityInfo.class}">
          <div class="ddi-alert-header">
            <span class="ddi-severity-badge">${alert.severityInfo.label}</span>
            <span class="ddi-summary">${escapeHtml(alert.summary)}</span>
          </div>
          <div class="ddi-alert-body">
            <p class="ddi-detail">${escapeHtml(alert.detail)}</p>
            <p class="ddi-recommendation"><strong>建議：</strong>${escapeHtml(alert.recommendation)}</p>
          </div>
          <div class="ddi-alert-footer">
            <span class="ddi-source">來源：${escapeHtml(alert.source)}</span>
          </div>
        </div>
      `;
    });

    html += '</div>';
    return html;
  }

  /**
   * Format alerts for CDS Hooks response
   */
  function formatForCDSHooks(alerts) {
    return alerts.map((alert, index) => ({
      uuid: `ddi-alert-${index}`,
      summary: alert.summary,
      indicator: alert.severity === 'Major' ? 'critical' : alert.severity === 'Moderate' ? 'warning' : 'info',
      detail: `${alert.detail}\n\n建議：${alert.recommendation}`,
      source: {
        label: 'JpTxGNN DDI Checker',
        url: 'https://jptxgnn.yao.care/'
      }
    }));
  }

  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Export
  global.JpTxGNN = global.JpTxGNN || {};
  global.JpTxGNN.DDIChecker = {
    load: loadDDIIndex,
    checkInteractions: checkInteractions,
    checkNewDrug: checkNewDrug,
    formatAlertsHTML: formatAlertsHTML,
    formatForCDSHooks: formatForCDSHooks,
    SEVERITY: SEVERITY
  };

  // Auto-load when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadDDIIndex);
  } else {
    loadDDIIndex();
  }

})(typeof window !== 'undefined' ? window : this);
