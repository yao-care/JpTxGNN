/**
 * Drug Lookup - 藥物查詢功能
 * 使用 Fuse.js 進行模糊搜尋，支援藥物名稱和適應症查詢
 */
(function() {
  'use strict';

  // 等待 DOM 和 Fuse.js 載入完成
  if (typeof Fuse === 'undefined') {
    console.error('Fuse.js not loaded');
    return;
  }

  const config = window.TWTXGNN_CONFIG || {
    searchIndexUrl: '/data/search-index.json',
    drugsBaseUrl: '/drugs/'
  };

  let searchIndex = null;
  let drugFuse = null;
  let indicationFuse = null;

  // DOM 元素
  const input = document.getElementById('lookup-input');
  const searchBtn = document.getElementById('lookup-search');
  const clearBtn = document.getElementById('lookup-clear');
  const results = document.getElementById('lookup-results');
  const levelFilters = document.querySelectorAll('.level-filter');

  if (!input || !results) {
    console.error('Drug lookup elements not found');
    return;
  }

  // 載入搜尋索引
  fetch(config.searchIndexUrl)
    .then(r => {
      if (!r.ok) throw new Error('Failed to fetch search index');
      return r.json();
    })
    .then(data => {
      searchIndex = data;

      // 初始化 Fuse.js
      drugFuse = new Fuse(data.drugs, {
        keys: ['name', 'brands', 'original'],
        threshold: 0.25,
        includeScore: true
      });

      indicationFuse = new Fuse(data.indications, {
        keys: ['name'],
        threshold: 0.25,
        includeScore: true
      });

      console.log('Search index loaded:', data.drug_count, 'drugs,', data.indication_count, 'indications');
    })
    .catch(e => {
      console.error('Failed to load search index:', e);
      results.innerHTML = '<div class="lookup-notice">Failed to load the search index. Please reload the page.</div>';
    });

  // 工具函數
  function getSelectedLevels() {
    return Array.from(levelFilters)
      .filter(cb => cb.checked)
      .map(cb => cb.value);
  }

  function filterByLevel(items, levels) {
    return items.filter(item => levels.includes(item.level));
  }

  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // 渲染搜尋結果
  function renderResults(query, showHint) {
    if (!searchIndex) {
      results.innerHTML = '<div class="lookup-notice">Loading the search index, please wait...</div>';
      return;
    }

    if (!query || query.length < 2) {
      if (showHint) {
        results.innerHTML = '<div class="lookup-notice">Please enter at least 2 characters</div>';
      } else {
        results.innerHTML = '';
      }
      return;
    }

    const levels = getSelectedLevels();
    if (levels.length === 0) {
      results.innerHTML = '<div class="lookup-notice">Please select at least one evidence level</div>';
      return;
    }

    let html = '';

    // 搜尋藥物
    const drugResults = drugFuse.search(query).slice(0, 5);
    const filteredDrugs = drugResults.filter(r => levels.includes(r.item.level));

    if (filteredDrugs.length > 0) {
      html += '<div class="result-section"><div class="section-title">Matching drugs</div>';
      filteredDrugs.forEach(r => {
        const drug = r.item;
        const brands = drug.brands && drug.brands.length > 0
          ? ' (' + drug.brands.slice(0, 2).join('、') + ')'
          : '';
        const filteredInds = filterByLevel(drug.indications || [], levels);

        html += '<div class="result-card">';
        html += '<div class="result-header">';
        html += '<a href="' + config.drugsBaseUrl + drug.slug + '/" class="drug-name">' + escapeHtml(drug.name) + escapeHtml(brands) + '</a>';
        html += '<span class="level-badge level-' + drug.level + '">' + drug.level + '</span>';
        html += '</div>';
        html += '<div class="result-original">Original indication: ' + (escapeHtml(drug.original) || '—') + '</div>';
        html += '<div class="result-indications"><strong>Predicted new indications:</strong> ';

        if (filteredInds.length > 0) {
          filteredInds.slice(0, 5).forEach(ind => {
            html += '<span class="ind-item"><span class="level-badge level-' + ind.level + '">' + ind.level + '</span> ' + escapeHtml(ind.name) + ' (' + ind.score + '%)</span>';
          });
          if (filteredInds.length > 5) {
            html += '<span class="more">...' + filteredInds.length + ' in total</span>';
          }
        } else {
          html += '<span class="no-match">(none match the filter)</span>';
        }

        html += '</div>';
        html += '<a href="' + config.drugsBaseUrl + drug.slug + '/" class="view-report">View full report →</a>';
        html += '</div>';
      });
      html += '</div>';
    }

    // 搜尋適應症
    const indResults = indicationFuse.search(query).slice(0, 5);
    const filteredInds = indResults.filter(r => levels.includes(r.item.level));

    if (filteredInds.length > 0) {
      html += '<div class="result-section"><div class="section-title">Matching indications</div>';
      filteredInds.forEach(r => {
        const ind = r.item;
        const indDrugs = filterByLevel(ind.drugs || [], levels);

        html += '<div class="result-card">';
        html += '<div class="result-header">';
        html += '<span class="indication-name">' + escapeHtml(ind.name) + '</span>';
        html += '<span class="level-badge level-' + ind.level + '">' + ind.level + '</span>';
        html += '</div>';
        html += '<div class="result-drugs"><strong>Candidate drugs (' + indDrugs.length + '):</strong> ';

        indDrugs.slice(0, 5).forEach(d => {
          html += '<div class="drug-item">';
          html += '<a href="' + config.drugsBaseUrl + d.slug + '/">' + escapeHtml(d.name) + '</a>';
          html += '<span class="level-badge level-' + d.level + '">' + d.level + '</span>';
          html += '<span class="score">' + d.score + '%</span>';
          html += '<span class="original-hint">' + escapeHtml(d.original) + '</span>';
          html += '</div>';
        });

        if (indDrugs.length > 5) {
          html += '<div class="more">...' + indDrugs.length + ' drugs in total</div>';
        }

        html += '</div></div>';
      });
      html += '</div>';
    }

    if (!html) {
      html = '<div class="lookup-notice">No matching results</div>';
    }

    results.innerHTML = html;
  }

  // 執行搜尋
  function doSearch() {
    renderResults(input.value.trim(), true);
  }

  // 事件監聽
  let debounceTimer;

  input.addEventListener('input', function() {
    if (clearBtn) {
      clearBtn.style.display = this.value ? 'block' : 'none';
    }
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function() {
      renderResults(input.value.trim(), false);
    }, 300);
  });

  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      doSearch();
    }
  });

  if (searchBtn) {
    searchBtn.addEventListener('click', doSearch);
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', function() {
      input.value = '';
      clearBtn.style.display = 'none';
      results.innerHTML = '';
      input.focus();
    });
  }

  levelFilters.forEach(function(cb) {
    cb.addEventListener('change', function() {
      renderResults(input.value.trim(), false);
    });
  });

})();
