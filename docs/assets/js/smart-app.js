/**
 * TwTxGNN SMART App Main Logic
 *
 * Handles FHIR client initialization, medication retrieval,
 * and UI rendering for drug repurposing candidates.
 */
(function(global) {
  'use strict';

  const CONFIG = {
    searchIndexUrl: '/data/search-index.json',
    drugsBaseUrl: '/drugs/'
  };

  // UI Elements
  let elements = {};

  // State
  let fhirClient = null;
  let drugMapper = null;
  let searchIndex = null;
  let patientMedications = [];
  let mappingResults = [];

  /**
   * Initialize the SMART App
   */
  async function init() {
    elements = {
      loading: document.getElementById('loading'),
      error: document.getElementById('error'),
      content: document.getElementById('content'),
      patientInfo: document.getElementById('patient-info'),
      medList: document.getElementById('medication-list'),
      results: document.getElementById('repurposing-results'),
      queryBtn: document.getElementById('query-btn'),
      selectAllBtn: document.getElementById('select-all-btn')
    };

    try {
      showLoading('載入藥物資料庫...');

      // Load search index
      searchIndex = await loadSearchIndex();

      showLoading('連線至 EHR 系統...');

      // Initialize FHIR client
      fhirClient = await FHIR.oauth2.ready();

      // Initialize drug mapper
      drugMapper = new TwTxGNN.DrugMapper(searchIndex);

      showLoading('讀取病患用藥資料...');

      // Load patient info and medications
      await loadPatientData();

      // Show main content
      showContent();

      // Setup event listeners
      setupEventListeners();

    } catch (error) {
      console.error('SMART App initialization error:', error);
      showError('無法初始化應用程式: ' + (error.message || error));
    }
  }

  /**
   * Load TwTxGNN search index
   */
  async function loadSearchIndex() {
    const response = await fetch(CONFIG.searchIndexUrl);
    if (!response.ok) {
      throw new Error('無法載入藥物資料庫');
    }
    return response.json();
  }

  /**
   * Load patient information and medications
   */
  async function loadPatientData() {
    // Get patient info
    const patient = await fhirClient.patient.read();
    renderPatientInfo(patient);

    // Get medications (try MedicationRequest first, then MedicationStatement)
    let medications = [];

    try {
      const medRequests = await fhirClient.request(
        `MedicationRequest?patient=${fhirClient.patient.id}&status=active,completed`,
        { flat: true }
      );
      if (Array.isArray(medRequests)) {
        medications = medications.concat(medRequests);
      }
    } catch (e) {
      console.warn('Could not fetch MedicationRequest:', e);
    }

    try {
      const medStatements = await fhirClient.request(
        `MedicationStatement?patient=${fhirClient.patient.id}&status=active,completed`,
        { flat: true }
      );
      if (Array.isArray(medStatements)) {
        medications = medications.concat(medStatements);
      }
    } catch (e) {
      console.warn('Could not fetch MedicationStatement:', e);
    }

    patientMedications = medications;

    // Map medications to TwTxGNN
    mappingResults = await drugMapper.mapMedications(medications);

    // Render medication list
    renderMedicationList();
  }

  /**
   * Render patient information
   */
  function renderPatientInfo(patient) {
    if (!elements.patientInfo) return;

    const name = patient.name?.[0];
    const displayName = name ?
      `${name.family || ''}, ${name.given?.join(' ') || ''}`.trim() :
      '未知';

    const birthDate = patient.birthDate || '未知';
    const gender = {
      'male': '男',
      'female': '女',
      'other': '其他',
      'unknown': '未知'
    }[patient.gender] || patient.gender || '未知';

    elements.patientInfo.innerHTML = `
      <div class="patient-card">
        <div class="patient-name">${escapeHtml(displayName)}</div>
        <div class="patient-details">
          <span>出生日期: ${escapeHtml(birthDate)}</span>
          <span>性別: ${escapeHtml(gender)}</span>
        </div>
      </div>
    `;
  }

  /**
   * Render medication list with checkboxes
   */
  function renderMedicationList() {
    if (!elements.medList) return;

    if (mappingResults.length === 0) {
      elements.medList.innerHTML = `
        <div class="empty-state">
          <p>未找到病患用藥記錄</p>
        </div>
      `;
      return;
    }

    let html = '<div class="med-list">';

    mappingResults.forEach((result, index) => {
      const displayName = result.displayName || result.ingredientName || '未知藥物';
      const matchStatus = result.matched ?
        `<span class="match-badge matched">有預測資料</span>` :
        `<span class="match-badge unmatched">無預測資料</span>`;

      const twtxgnnInfo = result.twtxgnnMatch ?
        `<span class="twtxgnn-name">→ ${escapeHtml(result.twtxgnnMatch.name)}</span>
         <span class="level-badge level-${result.twtxgnnMatch.level}">${result.twtxgnnMatch.level}</span>` :
        '';

      html += `
        <div class="med-item ${result.matched ? 'has-match' : 'no-match'}">
          <label class="med-label">
            <input type="checkbox" class="med-checkbox" data-index="${index}"
                   ${result.matched ? 'checked' : 'disabled'}>
            <span class="med-name">${escapeHtml(displayName)}</span>
            ${matchStatus}
          </label>
          <div class="med-mapping">
            ${twtxgnnInfo}
          </div>
        </div>
      `;
    });

    html += '</div>';
    elements.medList.innerHTML = html;
  }

  /**
   * Query repurposing candidates for selected medications
   */
  function queryRepurposingCandidates() {
    const checkboxes = document.querySelectorAll('.med-checkbox:checked');
    const selectedIndices = Array.from(checkboxes).map(cb => parseInt(cb.dataset.index));

    if (selectedIndices.length === 0) {
      elements.results.innerHTML = `
        <div class="empty-state">
          <p>請至少選擇一個藥物</p>
        </div>
      `;
      return;
    }

    let html = '';

    selectedIndices.forEach(index => {
      const result = mappingResults[index];
      if (!result.twtxgnnMatch) return;

      const drug = result.twtxgnnMatch;
      const indications = drug.indications || [];

      html += `
        <div class="drug-result-card">
          <div class="drug-header">
            <h3>
              <a href="${CONFIG.drugsBaseUrl}${drug.slug}/" target="_blank">
                ${escapeHtml(drug.name)}
              </a>
              <span class="level-badge level-${drug.level}">${drug.level}</span>
            </h3>
            <a href="${CONFIG.drugsBaseUrl}${drug.slug}/" target="_blank" class="view-full">
              查看完整報告 →
            </a>
          </div>

          <div class="drug-original">
            <strong>原適應症：</strong>
            ${escapeHtml(drug.original) || '—'}
          </div>

          <div class="drug-indications">
            <strong>預測新適應症（老藥新用候選）：</strong>
            <div class="indication-list">
      `;

      if (indications.length > 0) {
        indications.slice(0, 10).forEach(ind => {
          html += `
            <div class="indication-item">
              <span class="level-badge level-${ind.level}">${ind.level}</span>
              <span class="ind-name">${escapeHtml(ind.name)}</span>
              <span class="ind-score">${ind.score}%</span>
            </div>
          `;
        });

        if (indications.length > 10) {
          html += `
            <div class="more-indications">
              ...及其他 ${indications.length - 10} 個預測適應症
              <a href="${CONFIG.drugsBaseUrl}${drug.slug}/" target="_blank">查看全部</a>
            </div>
          `;
        }
      } else {
        html += '<p class="no-indications">無預測新適應症</p>';
      }

      html += `
            </div>
          </div>
        </div>
      `;
    });

    if (!html) {
      html = `
        <div class="empty-state">
          <p>選取的藥物無預測資料</p>
        </div>
      `;
    }

    elements.results.innerHTML = html;
  }

  /**
   * Setup event listeners
   */
  function setupEventListeners() {
    if (elements.queryBtn) {
      elements.queryBtn.addEventListener('click', queryRepurposingCandidates);
    }

    if (elements.selectAllBtn) {
      elements.selectAllBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.med-checkbox:not(:disabled)');
        const allChecked = Array.from(checkboxes).every(cb => cb.checked);

        checkboxes.forEach(cb => {
          cb.checked = !allChecked;
        });
      });
    }
  }

  // UI Helper functions
  function showLoading(message) {
    if (elements.loading) {
      elements.loading.style.display = 'flex';
      elements.loading.querySelector('.loading-text').textContent = message || '載入中...';
    }
    if (elements.error) elements.error.style.display = 'none';
    if (elements.content) elements.content.style.display = 'none';
  }

  function showError(message) {
    if (elements.loading) elements.loading.style.display = 'none';
    if (elements.error) {
      elements.error.style.display = 'block';
      elements.error.querySelector('.error-message').textContent = message;
    }
    if (elements.content) elements.content.style.display = 'none';
  }

  function showContent() {
    if (elements.loading) elements.loading.style.display = 'none';
    if (elements.error) elements.error.style.display = 'none';
    if (elements.content) elements.content.style.display = 'block';
  }

  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Export
  global.TwTxGNN = global.TwTxGNN || {};
  global.TwTxGNN.SmartApp = {
    init: init
  };

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})(typeof window !== 'undefined' ? window : this);
