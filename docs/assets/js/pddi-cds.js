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
      clinicalConsequence: 'Increased risk of gastrointestinal and systemic bleeding',
      frequency: 'Common (about 10-15% of users have clinically significant bleeding)',
      mechanism: 'NSAIDs inhibit platelet function and may enhance the anticoagulant effect of warfarin',
      contextualFactors: [
        {
          factor: 'History of GI bleeding',
          impact: 'Risk substantially increased',
          recommendation: 'Strongly advise avoiding the combination'
        },
        {
          factor: 'Age > 65 years',
          impact: 'Risk increased',
          recommendation: 'If required, add PPI protection'
        },
        {
          factor: 'Taking a PPI/H2 blocker',
          impact: 'Risk reduced',
          recommendation: 'Short-term use may be considered'
        },
        {
          factor: 'Unstable INR control',
          impact: 'Risk increased',
          recommendation: 'Avoid the combination'
        }
      ],
      managementOptions: [
        {
          option: 'Use acetaminophen instead',
          description: 'For pain management, acetaminophen is the safer choice',
          recommended: true
        },
        {
          option: 'Add a PPI',
          description: 'If an NSAID is required, add a PPI (e.g. omeprazole) to reduce GI bleeding risk',
          recommended: true
        },
        {
          option: 'Use a COX-2 inhibitor',
          description: 'Celecoxib carries a relatively lower GI risk, but caution is still needed',
          recommended: false
        },
        {
          option: 'Short-term use with close monitoring',
          description: 'Use the lowest effective dose for the shortest time and monitor for signs of bleeding',
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
      clinicalConsequence: 'Severe colchicine toxicity (bone marrow suppression, neuropathy, multi-organ failure)',
      frequency: 'Rare but potentially fatal',
      mechanism: 'CYP3A4 inhibitors greatly increase colchicine blood levels (up to 2-4 fold)',
      contextualFactors: [
        {
          factor: 'Renal impairment',
          impact: 'Combination contraindicated',
          recommendation: 'Absolute contraindication'
        },
        {
          factor: 'Hepatic impairment',
          impact: 'Combination contraindicated',
          recommendation: 'Absolute contraindication'
        },
        {
          factor: 'Normal renal and hepatic function',
          impact: 'Risk remains high',
          recommendation: 'Substantially reduce the colchicine dose or avoid'
        }
      ],
      managementOptions: [
        {
          option: 'Avoid the combination',
          description: 'Choose an alternative antibiotic or antifungal',
          recommended: true
        },
        {
          option: 'Reduce the colchicine dose',
          description: 'If the combination is necessary, reduce colchicine to 0.3 mg daily or lower',
          recommended: false
        },
        {
          option: 'Pause colchicine',
          description: 'Pause colchicine while a strong CYP3A4 inhibitor is being used',
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
      clinicalConsequence: 'Severe hypotension, excessive sedation',
      frequency: 'AUC increases 10-fold with ciprofloxacin',
      mechanism: 'CYP1A2 inhibitors markedly increase tizanidine bioavailability',
      contextualFactors: [
        {
          factor: 'Taking ciprofloxacin',
          impact: 'Combination contraindicated',
          recommendation: 'Switch to another antibiotic'
        },
        {
          factor: 'Taking fluvoxamine',
          impact: 'Combination contraindicated',
          recommendation: 'Switch to another SSRI'
        }
      ],
      managementOptions: [
        {
          option: 'Avoid the combination',
          description: 'Choose an alternative that does not inhibit CYP1A2',
          recommended: true
        },
        {
          option: 'Alternative muscle relaxant',
          description: 'Use baclofen or cyclobenzaprine instead',
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
      clinicalConsequence: 'Digoxin toxicity (arrhythmia, nausea and vomiting, visual disturbances)',
      frequency: 'Digoxin levels increase by 70% on average',
      mechanism: 'Amiodarone inhibits renal and non-renal clearance of digoxin',
      contextualFactors: [
        {
          factor: 'Renal impairment',
          impact: 'Risk increased',
          recommendation: 'Reduce the digoxin dose more aggressively'
        },
        {
          factor: 'Electrolyte disturbance (hypokalaemia)',
          impact: 'Risk substantially increased',
          recommendation: 'Correct electrolytes and monitor closely'
        }
      ],
      managementOptions: [
        {
          option: 'Reduce the digoxin dose by 50%',
          description: 'Halve the digoxin dose as soon as amiodarone is started',
          recommended: true
        },
        {
          option: 'Monitor digoxin levels',
          description: 'Monitor blood levels regularly; target 0.5-1.0 ng/mL',
          recommended: true
        },
        {
          option: 'Monitor the ECG',
          description: 'Watch for bradycardia and arrhythmia',
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
      clinicalConsequence: 'Torsades de pointes (polymorphic ventricular tachycardia)',
      frequency: 'Rare but potentially fatal',
      mechanism: 'Additive effect of multiple QT-prolonging drugs',
      contextualFactors: [
        {
          factor: 'Electrolyte disturbance',
          impact: 'Risk substantially increased',
          recommendation: 'Correct hypokalaemia and hypomagnesaemia'
        },
        {
          factor: 'Baseline QTc > 450 ms',
          impact: 'Combination contraindicated',
          recommendation: 'Avoid adding QT-prolonging drugs'
        },
        {
          factor: 'Female',
          impact: 'Risk increased',
          recommendation: 'Monitor more carefully'
        },
        {
          factor: 'History of heart disease',
          impact: 'Risk increased',
          recommendation: 'Consider alternative drugs'
        }
      ],
      managementOptions: [
        {
          option: 'Avoid the combination',
          description: 'Choose alternatives that do not prolong QT',
          recommended: true
        },
        {
          option: 'ECG monitoring',
          description: 'If the combination is necessary, monitor the QTc interval regularly',
          recommended: true
        },
        {
          option: 'Correct electrolytes',
          description: 'Keep serum potassium > 4.0 mEq/L and magnesium > 2.0 mg/dL',
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
          label: 'View full information',
          url: `https://jptxgnn.yao.care/drugs/`,
          type: 'absolute'
        }
      ],
      overrideReasons: [
        { code: 'patient-aware', display: 'Patient is aware of the risk' },
        { code: 'benefit-outweighs', display: 'Benefit outweighs risk' },
        { code: 'alternative-unavailable', display: 'No alternative available' },
        { code: 'monitoring-in-place', display: 'Monitoring plan in place' }
      ]
    };

    return card;
  }

  /**
   * Generate detailed markdown for PDDI alert
   */
  function generateDetailMarkdown(pddi) {
    let md = `## Drug interaction alert\n\n`;
    md += `**Interaction type**: ${getAlertTypeLabel(pddi.alertType)}\n\n`;
    md += `**Mechanism**: ${pddi.mechanism}\n\n`;
    md += `**Clinical consequence**: ${pddi.clinicalConsequence}\n\n`;
    md += `**Frequency**: ${pddi.frequency}\n\n`;

    md += `### Contextual factors\n\n`;
    pddi.contextualFactors.forEach(cf => {
      md += `- **${cf.factor}**: ${cf.impact} - ${cf.recommendation}\n`;
    });

    md += `\n### Management options\n\n`;
    pddi.managementOptions.forEach(opt => {
      const marker = opt.recommended ? '✓' : '○';
      md += `- ${marker} **${opt.option}**: ${opt.description}\n`;
    });

    md += `\n### Evidence level\n\n`;
    md += `Level: ${pddi.evidence.level}\n`;
    md += `Sources: ${pddi.evidence.sources.join(', ')}\n`;

    return md;
  }

  /**
   * Get human-readable alert type label
   */
  function getAlertTypeLabel(type) {
    const labels = {
      contraindicated: 'Contraindicated',
      conditional: 'Conditional alert',
      relative: 'Relative contraindication'
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
          <strong>Mechanism:</strong> ${escapeHtml(pddi.mechanism)}
        </div>
        <div class="pddi-context">
          <strong>Contextual factors:</strong>
          <ul>
    `;

    pddi.contextualFactors.forEach(cf => {
      html += `<li><strong>${escapeHtml(cf.factor)}：</strong>${escapeHtml(cf.impact)} - ${escapeHtml(cf.recommendation)}</li>`;
    });

    html += `
          </ul>
        </div>
        <div class="pddi-management">
          <strong>Recommended management:</strong>
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
          <strong>Evidence level:</strong> ${pddi.evidence.level} |
          <strong>Sources:</strong> ${pddi.evidence.sources.join(', ')}
        </div>
      </div>
    `;

    return html;
  }

  function getIndicatorLabel(indicator) {
    const labels = {
      critical: '⚠️ Critical',
      warning: '⚡ Warning',
      info: 'ℹ️ Info'
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
