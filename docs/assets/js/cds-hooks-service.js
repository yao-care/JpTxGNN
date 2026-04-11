/**
 * JpTxGNN CDS Hooks Service
 *
 * Client-side implementation of CDS Hooks service for static site deployment.
 * Can be used as a reference implementation or integrated with server-side services.
 *
 * Implements:
 * - order-sign: DDI checking and drug repurposing suggestions
 * - patient-view: Clinical trial matching
 *
 * @author JpTxGNN Team
 * @version 1.0.0
 */
(function(global) {
  'use strict';

  const CONFIG = {
    serviceUrl: 'https://jptxgnn.yao.care/cds-hooks/',
    fhirBaseUrl: 'https://jptxgnn.yao.care/fhir/'
  };

  /**
   * CDS Hooks Service Discovery Response
   */
  const SERVICES = {
    services: [
      {
        hook: 'order-sign',
        title: 'JpTxGNN 藥物交互作用檢查',
        description: '基於 DDInter 2.0 資料庫，檢查處方中的潛在藥物交互作用',
        id: 'jptxgnn-ddi-check',
        prefetch: {
          patient: 'Patient/{{context.patientId}}',
          medications: 'MedicationRequest?patient={{context.patientId}}&status=active,completed'
        }
      },
      {
        hook: 'order-sign',
        title: 'JpTxGNN 老藥新用候選',
        description: '基於 TxGNN 知識圖譜，提供病患用藥的老藥新用預測',
        id: 'jptxgnn-repurposing',
        prefetch: {
          patient: 'Patient/{{context.patientId}}',
          medications: 'MedicationRequest?patient={{context.patientId}}&status=active,completed',
          conditions: 'Condition?patient={{context.patientId}}&clinical-status=active'
        }
      }
    ]
  };

  /**
   * Extract medication names from FHIR resources
   */
  function extractMedicationNames(prefetch) {
    const names = [];

    if (prefetch?.medications?.entry) {
      prefetch.medications.entry.forEach(entry => {
        const resource = entry.resource;
        if (resource?.medicationCodeableConcept?.coding) {
          resource.medicationCodeableConcept.coding.forEach(coding => {
            if (coding.display) {
              names.push(coding.display);
            }
          });
        }
        if (resource?.medicationCodeableConcept?.text) {
          names.push(resource.medicationCodeableConcept.text);
        }
      });
    }

    // Also check draftOrders in context
    return [...new Set(names)];
  }

  /**
   * Extract drug from draft order
   */
  function extractDraftOrderDrug(context) {
    if (context?.draftOrders?.entry) {
      for (const entry of context.draftOrders.entry) {
        const resource = entry.resource;
        if (resource?.resourceType === 'MedicationRequest') {
          if (resource.medicationCodeableConcept?.coding?.[0]?.display) {
            return resource.medicationCodeableConcept.coding[0].display;
          }
          if (resource.medicationCodeableConcept?.text) {
            return resource.medicationCodeableConcept.text;
          }
        }
      }
    }
    return null;
  }

  /**
   * Process order-sign hook for DDI checking
   */
  function processOrderSignDDI(request) {
    const cards = [];

    // Get current medications
    const currentMeds = extractMedicationNames(request.prefetch);

    // Get new medication from draft order
    const newMed = extractDraftOrderDrug(request.context);

    if (!newMed || currentMeds.length === 0) {
      return { cards };
    }

    // Check for PDDI using JpTxGNN.PDDI if available
    if (global.JpTxGNN?.PDDI) {
      const allMeds = [...currentMeds, newMed];
      const pddiAlerts = global.JpTxGNN.PDDI.checkPDDI(allMeds);

      pddiAlerts.forEach(pddi => {
        const card = global.JpTxGNN.PDDI.generateCDSHooksCard(pddi);
        cards.push(card);
      });
    }

    // Also check with basic DDI checker
    if (global.JpTxGNN?.DDIChecker) {
      const ddiAlerts = global.JpTxGNN.DDIChecker.checkNewDrug(newMed, currentMeds);

      ddiAlerts.forEach(alert => {
        // Avoid duplicates with PDDI
        const isDuplicate = cards.some(c =>
          c.summary.toLowerCase().includes(alert.drug1.toLowerCase()) &&
          c.summary.toLowerCase().includes(alert.drug2.toLowerCase())
        );

        if (!isDuplicate) {
          cards.push({
            uuid: `ddi-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            summary: alert.summary,
            indicator: alert.severity === 'Major' ? 'critical' : 'warning',
            detail: `${alert.detail}\n\n**建議：** ${alert.recommendation}`,
            source: {
              label: 'JpTxGNN DDI Checker',
              url: 'https://jptxgnn.yao.care/'
            }
          });
        }
      });
    }

    return { cards };
  }

  /**
   * Process order-sign hook for drug repurposing
   */
  function processOrderSignRepurposing(request) {
    const cards = [];

    // Get medications
    const currentMeds = extractMedicationNames(request.prefetch);
    const newMed = extractDraftOrderDrug(request.context);

    const allMeds = newMed ? [...currentMeds, newMed] : currentMeds;

    if (allMeds.length === 0) {
      return { cards };
    }

    // Check for repurposing candidates using DrugMapper
    if (global.JpTxGNN?.DrugMapper) {
      // This would need the search index to be loaded
      // For now, return a link card
      cards.push({
        uuid: `repurposing-info-${Date.now()}`,
        summary: '查看老藥新用候選預測',
        indicator: 'info',
        detail: `您正在處方的藥物可能有已知的老藥新用候選。點擊連結查看詳細預測資訊。`,
        source: {
          label: 'JpTxGNN Drug Repurposing',
          url: 'https://jptxgnn.yao.care/'
        },
        links: [
          {
            label: '查看老藥新用預測',
            url: `https://jptxgnn.yao.care/smart/standalone.html?drugs=${encodeURIComponent(allMeds.join(','))}`,
            type: 'absolute'
          }
        ]
      });
    }

    return { cards };
  }

  /**
   * Process patient-view hook for clinical trial matching
   */
  function processPatientView(request) {
    const cards = [];

    // Extract conditions
    const conditions = [];
    if (request.prefetch?.conditions?.entry) {
      request.prefetch.conditions.entry.forEach(entry => {
        const resource = entry.resource;
        if (resource?.code?.coding) {
          resource.code.coding.forEach(coding => {
            if (coding.display) {
              conditions.push(coding.display);
            }
          });
        }
      });
    }

    // Extract medications
    const medications = extractMedicationNames(request.prefetch);

    if (conditions.length > 0 || medications.length > 0) {
      cards.push({
        uuid: `trial-match-${Date.now()}`,
        summary: '🔬 可能有相關臨床試驗',
        indicator: 'info',
        detail: `根據病患的診斷和用藥，可能有相關的臨床試驗。\n\n` +
                `**診斷：** ${conditions.join(', ') || '無'}\n` +
                `**用藥：** ${medications.join(', ') || '無'}`,
        source: {
          label: 'JpTxGNN Clinical Trial Match',
          url: 'https://jptxgnn.yao.care/'
        },
        links: [
          {
            label: '搜尋 ClinicalTrials.gov',
            url: `https://clinicaltrials.gov/search?cond=${encodeURIComponent(conditions.join(' '))}`,
            type: 'absolute'
          },
          {
            label: '查看老藥新用預測',
            url: `https://jptxgnn.yao.care/smart/standalone.html?drugs=${encodeURIComponent(medications.join(','))}`,
            type: 'absolute'
          }
        ]
      });
    }

    return { cards };
  }

  /**
   * Main CDS Hooks request handler
   */
  function handleRequest(serviceId, request) {
    switch (serviceId) {
      case 'jptxgnn-ddi-check':
        return processOrderSignDDI(request);

      case 'jptxgnn-repurposing':
        return processOrderSignRepurposing(request);

      case 'jptxgnn-trial-match':
        return processPatientView(request);

      default:
        return { cards: [] };
    }
  }

  /**
   * Validate CDS Hooks request
   */
  function validateRequest(request) {
    const errors = [];

    if (!request.hook) {
      errors.push('Missing required field: hook');
    }

    if (!request.hookInstance) {
      errors.push('Missing required field: hookInstance');
    }

    if (!request.context) {
      errors.push('Missing required field: context');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Create a mock CDS Hooks request for testing
   */
  function createMockRequest(hook, medications, conditions) {
    return {
      hook: hook,
      hookInstance: `mock-${Date.now()}`,
      fhirServer: 'https://example.com/fhir',
      context: {
        userId: 'Practitioner/example',
        patientId: 'Patient/example',
        draftOrders: medications.length > 0 ? {
          resourceType: 'Bundle',
          entry: [{
            resource: {
              resourceType: 'MedicationRequest',
              medicationCodeableConcept: {
                text: medications[0],
                coding: [{
                  system: 'http://www.nlm.nih.gov/research/umls/rxnorm',
                  display: medications[0]
                }]
              }
            }
          }]
        } : undefined
      },
      prefetch: {
        medications: {
          resourceType: 'Bundle',
          entry: medications.slice(1).map(med => ({
            resource: {
              resourceType: 'MedicationRequest',
              medicationCodeableConcept: {
                text: med,
                coding: [{
                  system: 'http://www.nlm.nih.gov/research/umls/rxnorm',
                  display: med
                }]
              }
            }
          }))
        },
        conditions: conditions ? {
          resourceType: 'Bundle',
          entry: conditions.map(cond => ({
            resource: {
              resourceType: 'Condition',
              code: {
                text: cond,
                coding: [{
                  system: 'http://snomed.info/sct',
                  display: cond
                }]
              }
            }
          }))
        } : undefined
      }
    };
  }

  /**
   * Demo function to test CDS Hooks
   */
  function demo(medications, conditions) {
    console.log('=== JpTxGNN CDS Hooks Demo ===');
    console.log('Medications:', medications);
    console.log('Conditions:', conditions || []);

    // Test DDI check
    const ddiRequest = createMockRequest('order-sign', medications, null);
    const ddiResponse = handleRequest('jptxgnn-ddi-check', ddiRequest);
    console.log('\n--- DDI Check Response ---');
    console.log(JSON.stringify(ddiResponse, null, 2));

    // Test repurposing
    const repurposingResponse = handleRequest('jptxgnn-repurposing', ddiRequest);
    console.log('\n--- Repurposing Response ---');
    console.log(JSON.stringify(repurposingResponse, null, 2));

    // Test trial matching
    if (conditions) {
      const trialRequest = createMockRequest('patient-view', medications, conditions);
      const trialResponse = handleRequest('jptxgnn-trial-match', trialRequest);
      console.log('\n--- Trial Match Response ---');
      console.log(JSON.stringify(trialResponse, null, 2));
    }

    return {
      ddi: ddiResponse,
      repurposing: repurposingResponse
    };
  }

  // Export
  global.JpTxGNN = global.JpTxGNN || {};
  global.JpTxGNN.CDSHooks = {
    SERVICES: SERVICES,
    handleRequest: handleRequest,
    validateRequest: validateRequest,
    createMockRequest: createMockRequest,
    demo: demo
  };

})(typeof window !== 'undefined' ? window : this);
