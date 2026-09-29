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
    'Major': { priority: 3, class: 'ddi-major', label: 'Major' },
    'Moderate': { priority: 2, class: 'ddi-moderate', label: 'Moderate' },
    'Minor': { priority: 1, class: 'ddi-minor', label: 'Minor' }
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
      summary: 'Warfarin + Ibuprofen: increased bleeding risk',
      detail: 'NSAIDs inhibit platelet function and may enhance the anticoagulant effect of warfarin, significantly increasing the risk of gastrointestinal bleeding.',
      recommendation: 'Use acetaminophen instead, or add a PPI for gastric protection.'
    },
    {
      drugs: [
        ['warfarin', 'coumadin'],
        ['aspirin', 'acetylsalicylic acid']
      ],
      severity: 'Major',
      summary: 'Warfarin + Aspirin: increased bleeding risk',
      detail: 'Both affect haemostasis; combined use greatly increases the risk of bleeding.',
      recommendation: 'If the combination is necessary, use low-dose aspirin and monitor INR closely.'
    },
    {
      drugs: [
        ['warfarin', 'coumadin'],
        ['naproxen', 'aleve', 'naprosyn']
      ],
      severity: 'Major',
      summary: 'Warfarin + Naproxen: increased bleeding risk',
      detail: 'Combining naproxen with warfarin increases the risk of gastrointestinal and other bleeding events.',
      recommendation: 'Use acetaminophen for pain relief instead.'
    },
    {
      drugs: [
        ['metformin', 'glucophage'],
        ['iodixanol', 'visipaque', 'iopamidol', 'isovue', 'contrast']
      ],
      severity: 'Major',
      summary: 'Metformin + iodinated contrast media: risk of lactic acidosis',
      detail: 'Contrast media may cause acute kidney injury, leading to metformin accumulation and lactic acidosis.',
      recommendation: 'Stop metformin 48 hours before the procedure and restart only after renal function is confirmed normal.'
    },
    {
      drugs: [
        ['colchicine', 'colcrys'],
        ['clarithromycin', 'biaxin', 'klacid']
      ],
      severity: 'Major',
      summary: 'Colchicine + Clarithromycin: risk of toxicity',
      detail: 'Clarithromycin is a strong CYP3A4 inhibitor and greatly increases colchicine blood levels.',
      recommendation: 'Avoid the combination or substantially reduce the colchicine dose.'
    },
    {
      drugs: [
        ['colchicine', 'colcrys'],
        ['ritonavir', 'norvir', 'cobicistat', 'tybost']
      ],
      severity: 'Major',
      summary: 'Colchicine + HIV protease inhibitors: risk of severe toxicity',
      detail: 'HIV protease inhibitors markedly increase colchicine levels and may cause fatal toxicity.',
      recommendation: 'Contraindicated in patients with renal or hepatic impairment.'
    },
    {
      drugs: [
        ['simvastatin', 'zocor'],
        ['amiodarone', 'cordarone']
      ],
      severity: 'Major',
      summary: 'Simvastatin + Amiodarone: risk of myopathy',
      detail: 'Amiodarone increases simvastatin levels, raising the risk of rhabdomyolysis.',
      recommendation: 'Do not exceed simvastatin 20 mg/day, or switch to another statin.'
    },
    {
      drugs: [
        ['fluoxetine', 'prozac', 'sertraline', 'zoloft', 'paroxetine', 'paxil'],
        ['tramadol', 'ultram']
      ],
      severity: 'Major',
      summary: 'SSRI + Tramadol: risk of serotonin syndrome',
      detail: 'Both increase serotonergic activity; combined use may cause life-threatening serotonin syndrome.',
      recommendation: 'Monitor closely for symptoms (hyperthermia, myoclonus, altered mental status) and consider an alternative analgesic.'
    },
    {
      drugs: [
        ['fluoxetine', 'prozac', 'sertraline', 'zoloft', 'paroxetine', 'paxil'],
        ['linezolid', 'zyvox']
      ],
      severity: 'Major',
      summary: 'SSRI + Linezolid: risk of serotonin syndrome',
      detail: 'Linezolid is an MAO inhibitor; combining it with an SSRI is highly dangerous.',
      recommendation: 'Avoid the combination. If linezolid is required, stop the SSRI and allow an appropriate washout period.'
    },
    {
      drugs: [
        ['amiodarone', 'cordarone'],
        ['moxifloxacin', 'avelox']
      ],
      severity: 'Major',
      summary: 'Amiodarone + Moxifloxacin: risk of QT prolongation',
      detail: 'Both can prolong the QT interval; combined use increases the risk of torsades de pointes.',
      recommendation: 'Avoid the combination or monitor the ECG closely.'
    },
    {
      drugs: [
        ['digoxin', 'lanoxin'],
        ['amiodarone', 'cordarone']
      ],
      severity: 'Major',
      summary: 'Digoxin + Amiodarone: risk of digoxin toxicity',
      detail: 'Amiodarone increases digoxin blood levels by about 70%.',
      recommendation: 'When starting amiodarone, halve the digoxin dose and monitor blood levels.'
    },
    {
      drugs: [
        ['clopidogrel', 'plavix'],
        ['omeprazole', 'prilosec', 'esomeprazole', 'nexium']
      ],
      severity: 'Moderate',
      summary: 'Clopidogrel + PPI: reduced antiplatelet effect',
      detail: 'Omeprazole inhibits CYP2C19, reducing conversion of clopidogrel to its active metabolite.',
      recommendation: 'Consider pantoprazole or an H2 blocker instead.'
    },
    {
      drugs: [
        ['lithium', 'lithobid'],
        ['ibuprofen', 'advil', 'naproxen', 'aleve', 'diclofenac']
      ],
      severity: 'Major',
      summary: 'Lithium + NSAIDs: risk of lithium toxicity',
      detail: 'NSAIDs reduce renal excretion of lithium, raising its blood levels.',
      recommendation: 'Avoid the combination or monitor lithium levels closely.'
    },
    {
      drugs: [
        ['potassium', 'k-dur', 'klor-con'],
        ['spironolactone', 'aldactone', 'eplerenone', 'inspra']
      ],
      severity: 'Major',
      summary: 'Potassium supplements + potassium-sparing diuretics: risk of hyperkalaemia',
      detail: 'Both raise serum potassium; combined use may cause life-threatening hyperkalaemia.',
      recommendation: 'Monitor serum potassium regularly and avoid concurrent potassium supplementation.'
    },
    {
      drugs: [
        ['methotrexate', 'trexall'],
        ['trimethoprim', 'bactrim', 'septra', 'sulfamethoxazole']
      ],
      severity: 'Major',
      summary: 'Methotrexate + TMP-SMX: risk of bone marrow suppression',
      detail: 'Both inhibit folate metabolism; combined use increases the risk of bone marrow suppression and mucositis.',
      recommendation: 'Avoid the combination, or ensure adequate folate supplementation and monitor blood counts closely.'
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
      return '<div class="ddi-no-alerts">No drug interaction alerts found</div>';
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
            <p class="ddi-recommendation"><strong>Recommendation:</strong> ${escapeHtml(alert.recommendation)}</p>
          </div>
          <div class="ddi-alert-footer">
            <span class="ddi-source">Source: ${escapeHtml(alert.source)}</span>
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
      detail: `${alert.detail}\n\nRecommendation: ${alert.recommendation}`,
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
