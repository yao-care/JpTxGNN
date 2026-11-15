/**
 * JpTxGNN Drug-Drug Interaction Checker
 *
 * Client-side DDI checking with 15 built-in curated rules (DDInter consulted as a reference; not a full database lookup).
 * Provides real-time interaction alerts for drug repurposing candidates.
 *
 * @author JpTxGNN Team
 * @version 1.0.0
 */
(function(global) {
  'use strict';

  const CONFIG = {
    // This site does not publish /data/ddi-index.json; only the curated rules
    // below are used. Set a URL here once such a file exists.
    ddiDataUrl: null,
    maxAlerts: 10
  };

  // Severity levels with priority (higher = more severe)
  const SEVERITY = {
    'Major': { priority: 3, class: 'ddi-major', label: '重度' },
    'Moderate': { priority: 2, class: 'ddi-moderate', label: '中等度' },
    'Minor': { priority: 1, class: 'ddi-minor', label: '軽度' }
  };

  // 15 built-in high-priority DDI rules (hand-curated, DDInter consulted as a reference)
  // Format: { drug1: [synonym list], drug2: [synonym list], severity, summary, detail }
  const CURATED_DDI_RULES = [
    {
      drugs: [
        ['warfarin', 'coumadin'],
        ['ibuprofen', 'advil', 'motrin', 'brufen']
      ],
      severity: 'Major',
      summary: 'ワルファリン + イブプロフェン：出血リスクの増加',
      detail: 'NSAIDs は血小板機能を阻害し、ワルファリンの抗凝固作用を増強するおそれがあり、消化管出血のリスクが大きく高まります。',
      recommendation: '代わりにアセトアミノフェンを使用するか、胃粘膜保護のため PPI を併用してください。'
    },
    {
      drugs: [
        ['warfarin', 'coumadin'],
        ['aspirin', 'acetylsalicylic acid']
      ],
      severity: 'Major',
      summary: 'ワルファリン + アスピリン：出血リスクの増加',
      detail: 'いずれも止血機構に影響し、併用で出血リスクが大きく高まります。',
      recommendation: '併用が必要な場合は低用量アスピリンを使用し、INR を厳重に監視してください。'
    },
    {
      drugs: [
        ['warfarin', 'coumadin'],
        ['naproxen', 'aleve', 'naprosyn']
      ],
      severity: 'Major',
      summary: 'ワルファリン + ナプロキセン：出血リスクの増加',
      detail: 'ナプロキセンとワルファリンの併用で、消化管出血などの出血のリスクが高まります。',
      recommendation: '鎮痛には代わりにアセトアミノフェンを使用してください。'
    },
    {
      drugs: [
        ['metformin', 'glucophage'],
        ['iodixanol', 'visipaque', 'iopamidol', 'isovue', 'contrast']
      ],
      severity: 'Major',
      summary: 'メトホルミン + ヨード造影剤：乳酸アシドーシスのリスク',
      detail: '造影剤により急性腎障害が起こると、メトホルミンが蓄積して乳酸アシドーシスを来すおそれがあります。',
      recommendation: '検査の 48 時間前にメトホルミンを中止し、腎機能が正常であることを確認してから再開してください。'
    },
    {
      drugs: [
        ['colchicine', 'colcrys'],
        ['clarithromycin', 'biaxin', 'klacid']
      ],
      severity: 'Major',
      summary: 'コルヒチン + クラリスロマイシン：中毒のリスク',
      detail: 'クラリスロマイシンは強力な CYP3A4 阻害薬で、コルヒチンの血中濃度を大きく上昇させます。',
      recommendation: '併用を避けるか、コルヒチンの用量を大幅に減らしてください。'
    },
    {
      drugs: [
        ['colchicine', 'colcrys'],
        ['ritonavir', 'norvir', 'cobicistat', 'tybost']
      ],
      severity: 'Major',
      summary: 'コルヒチン + HIV プロテアーゼ阻害薬：重篤な中毒のリスク',
      detail: 'HIV プロテアーゼ阻害薬はコルヒチンの濃度を著しく上昇させ、致死的な中毒を起こすおそれがあります。',
      recommendation: '腎機能または肝機能障害のある患者には禁忌です。'
    },
    {
      drugs: [
        ['simvastatin', 'zocor'],
        ['amiodarone', 'cordarone']
      ],
      severity: 'Major',
      summary: 'シンバスタチン + アミオダロン：ミオパチーのリスク',
      detail: 'アミオダロンはシンバスタチンの濃度を上昇させ、横紋筋融解症のリスクを高めます。',
      recommendation: 'シンバスタチンは 1 日 20 mg を超えないようにするか、他のスタチンに変更してください。'
    },
    {
      drugs: [
        ['fluoxetine', 'prozac', 'sertraline', 'zoloft', 'paroxetine', 'paxil'],
        ['tramadol', 'ultram']
      ],
      severity: 'Major',
      summary: 'SSRI + トラマドール：セロトニン症候群のリスク',
      detail: 'いずれもセロトニン作用を強め、併用で生命を脅かすセロトニン症候群を起こすおそれがあります。',
      recommendation: '症状（高体温、ミオクローヌス、精神状態の変化）を注意深く観察し、他の鎮痛薬を検討してください。'
    },
    {
      drugs: [
        ['fluoxetine', 'prozac', 'sertraline', 'zoloft', 'paroxetine', 'paxil'],
        ['linezolid', 'zyvox']
      ],
      severity: 'Major',
      summary: 'SSRI + リネゾリド：セロトニン症候群のリスク',
      detail: 'リネゾリドは MAO 阻害作用をもち、SSRI との併用は非常に危険です。',
      recommendation: '併用を避けてください。リネゾリドが必要な場合は SSRI を中止し、適切な休薬期間をおいてください。'
    },
    {
      drugs: [
        ['amiodarone', 'cordarone'],
        ['moxifloxacin', 'avelox']
      ],
      severity: 'Major',
      summary: 'アミオダロン + モキシフロキサシン：QT 延長のリスク',
      detail: 'いずれも QT 間隔を延長させるおそれがあり、併用でトルサード・ド・ポアントのリスクが高まります。',
      recommendation: '併用を避けるか、心電図を注意深く監視してください。'
    },
    {
      drugs: [
        ['digoxin', 'lanoxin'],
        ['amiodarone', 'cordarone']
      ],
      severity: 'Major',
      summary: 'ジゴキシン + アミオダロン：ジゴキシン中毒のリスク',
      detail: 'アミオダロンはジゴキシンの血中濃度を約 70% 上昇させます。',
      recommendation: 'アミオダロン開始時はジゴキシンの用量を半分にし、血中濃度を監視してください。'
    },
    {
      drugs: [
        ['clopidogrel', 'plavix'],
        ['omeprazole', 'prilosec', 'esomeprazole', 'nexium']
      ],
      severity: 'Moderate',
      summary: 'クロピドグレル + PPI：抗血小板作用の減弱',
      detail: 'オメプラゾールは CYP2C19 を阻害し、クロピドグレルの活性代謝物への変換を低下させます。',
      recommendation: '代わりにパントプラゾールまたは H2 遮断薬を検討してください。'
    },
    {
      drugs: [
        ['lithium', 'lithobid'],
        ['ibuprofen', 'advil', 'naproxen', 'aleve', 'diclofenac']
      ],
      severity: 'Major',
      summary: 'リチウム + NSAIDs：リチウム中毒のリスク',
      detail: 'NSAIDs はリチウムの腎排泄を低下させ、血中濃度を上昇させます。',
      recommendation: '併用を避けるか、リチウム濃度を注意深く監視してください。'
    },
    {
      drugs: [
        ['potassium', 'k-dur', 'klor-con'],
        ['spironolactone', 'aldactone', 'eplerenone', 'inspra']
      ],
      severity: 'Major',
      summary: 'カリウム製剤 + カリウム保持性利尿薬：高カリウム血症のリスク',
      detail: 'いずれも血清カリウムを上昇させ、併用で生命を脅かす高カリウム血症を起こすおそれがあります。',
      recommendation: '血清カリウムを定期的に測定し、カリウム製剤の同時補充は避けてください。'
    },
    {
      drugs: [
        ['methotrexate', 'trexall'],
        ['trimethoprim', 'bactrim', 'septra', 'sulfamethoxazole']
      ],
      severity: 'Major',
      summary: 'メトトレキサート + ST 合剤：骨髄抑制のリスク',
      detail: 'いずれも葉酸代謝を阻害し、併用で骨髄抑制と粘膜炎のリスクが高まります。',
      recommendation: '併用を避けるか、十分な葉酸補充を行い、血球数を注意深く監視してください。'
    }
  ];

  let ddiIndex = null;
  let isLoaded = false;

  /**
   * Load DDI index data
   */
  async function loadDDIIndex() {
    if (isLoaded) return;
    if (!CONFIG.ddiDataUrl) {
      isLoaded = true;
      return;
    }

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
          source: 'JpTxGNN 内蔵の相互作用ルール（厳選 15 件。DDInter の全件照会ではありません）'
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
      return '<div class="ddi-no-alerts">相互作用の警告はありません</div>';
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
            <p class="ddi-recommendation"><strong>推奨：</strong> ${escapeHtml(alert.recommendation)}</p>
          </div>
          <div class="ddi-alert-footer">
            <span class="ddi-source">出典：${escapeHtml(alert.source)}</span>
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
      detail: `${alert.detail}\n\n推奨：${alert.recommendation}`,
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
