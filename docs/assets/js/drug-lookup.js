/**
 * Drug Lookup - 藥物查詢功能
 * 使用 Fuse.js 進行模糊搜尋，支援藥物名稱和適應症查詢
 */
(function() {
  'use strict';

  // Salt suffixes stripped before comparing names (same list as smart-fhir-mapper.js)
  const SALT_SUFFIXES = [
    ' HCL', ' HYDROCHLORIDE', ' SODIUM', ' POTASSIUM',
    ' SULFATE', ' SULPHATE', ' MALEATE', ' ACETATE',
    ' CITRATE', ' PHOSPHATE', ' BROMIDE', ' CHLORIDE',
    ' TARTRATE', ' FUMARATE', ' SUCCINATE', ' MESYLATE',
    ' BESYLATE', ' CALCIUM', ' MAGNESIUM', ' NITRATE',
    ' LACTATE', ' GLUCONATE', ' DISODIUM', ' MONOHYDRATE',
    ' DIHYDRATE', ' TRIHYDRATE', ' ANHYDROUS',
    ' DIPROPIONATE', ' PROPIONATE', ' ACETONIDE',
    ' VALERATE', ' BUTYRATE', ' HEXAHYDRATE',
    ' HBR', ' HYDROBROMIDE', ' MONONITRATE'
  ];

  // Synonym groups (INN / USAN / BAN spellings of the same substance).
  // Order inside a group does not matter: a query is resolved to whichever
  // spelling this site's search-index actually uses (e.g. ASPIRIN ->
  // "Acetylsalicylic Acid" when the index stores that name). Only exact
  // same-substance pairs belong here.
  const SYNONYM_GROUPS = [
    ['ACETYLSALICYLIC ACID', 'ASPIRIN'],
    ['PARACETAMOL', 'ACETAMINOPHEN'],
    ['ADRENALINE', 'EPINEPHRINE'],
    ['NORADRENALINE', 'NOREPINEPHRINE'],
    ['LIGNOCAINE', 'LIDOCAINE'],
    ['FRUSEMIDE', 'FUROSEMIDE'],
    ['SALBUTAMOL', 'ALBUTEROL'],
    ['GLIBENCLAMIDE', 'GLYBURIDE'],
    ['MESALAZINE', 'MESALAMINE'],
    ['CICLOSPORIN', 'CYCLOSPORINE'],
    ['RIFAMPICIN', 'RIFAMPIN'],
    ['ACICLOVIR', 'ACYCLOVIR'],
    ['VALACICLOVIR', 'VALACYCLOVIR'],
    ['CEFALEXIN', 'CEPHALEXIN'],
    ['PETHIDINE', 'MEPERIDINE'],
    ['HYOSCINE', 'SCOPOLAMINE'],
    ['ISOPRENALINE', 'ISOPROTERENOL'],
    ['GLYCERYL TRINITRATE', 'NITROGLYCERIN'],
    ['LEVOTHYROXINE', 'THYROXINE'],
    ['BENZATROPINE', 'BENZTROPINE'],
    ['CLOMIFENE', 'CLOMIPHENE'],
    ['DICYCLOVERINE', 'DICYCLOMINE'],
    ['TRIHEXYPHENIDYL', 'BENZHEXOL'],
    ['ESTRADIOL', 'OESTRADIOL'],
    ['COLECALCIFEROL', 'CHOLECALCIFEROL', 'VITAMIN D3'],
    ['ERGOCALCIFEROL', 'VITAMIN D2'],
    ['PHYTOMENADIONE', 'PHYTONADIONE', 'VITAMIN K1'],
    ['NIACINAMIDE', 'NICOTINAMIDE'],
    ['NICOTINIC ACID', 'NIACIN'],
    ['PYRIDOXINE', 'VITAMIN B6'],
    ['THIAMINE', 'VITAMIN B1'],
    ['RIBOFLAVIN', 'VITAMIN B2'],
    ['CYANOCOBALAMIN', 'VITAMIN B12'],
    ['ASCORBIC ACID', 'VITAMIN C'],
    ['TOCOPHEROL', 'VITAMIN E'],
    ['RETINOL', 'VITAMIN A'],
    ['LEVOMENTHOL', 'L-MENTHOL'],
    ['RACEMENTHOL', 'DL-MENTHOL'],
    ['DEXTROSE', 'GLUCOSE']
  ];

  // Counter-ion words: a name is never reduced to one of these alone
  // (e.g. "POTASSIUM CITRATE" must not become "POTASSIUM").
  const SALT_WORDS = new Set(SALT_SUFFIXES.map(s => s.trim()));

  function stripDiacritics(s) {
    return s.normalize('NFKD').replace(/[̀-ͯ]/g, '');
  }

  // Upper-case, strip accents and parenthetical text, collapse whitespace.
  function baseKey(name) {
    if (!name) return '';
    return stripDiacritics(String(name)).toUpperCase()
      .replace(/\s*\([^)]*\)/g, ' ')
      .replace(/[\s,;]+/g, ' ')
      .trim();
  }

  function stripSalt(key) {
    for (const suffix of SALT_SUFFIXES) {
      if (key.endsWith(suffix)) {
        const rest = key.slice(0, -suffix.length).trim();
        if (rest && !SALT_WORDS.has(rest)) return rest;
        return key;
      }
    }
    return key;
  }

  // Derived lookup keys for a base key: salt-stripped and L-/D-/DL- stripped.
  function derivedKeys(key) {
    const out = [];
    const add = k => { if (k && k !== key && !out.includes(k)) out.push(k); };
    const noSalt = stripSalt(key);
    add(noSalt);
    add(noSalt.replace(/^(DL-|L-|D-)/, ''));
    return out;
  }

  // "AMLODIPINE 5 MG ORAL TABLET" -> "AMLODIPINE"
  function stripDose(key) {
    const tokens = key.split(' ');
    const i = tokens.findIndex(t => /^\d/.test(t));
    return i > 0 ? tokens.slice(0, i).join(' ') : key;
  }

  function synonymsOf(key) {
    const group = SYNONYM_GROUPS.find(g => g.includes(key));
    return group ? group.filter(k => k !== key) : [];
  }


  // Exact lookup tables built from this site's search-index: exact names, then
  // salt/prefix-stripped names, then brand names. A key shared by two different
  // drugs is ambiguous and never used.
  function buildExactIndex(drugs) {
    const idx = { primary: new Map(), derived: new Map(), brand: new Map() };
    const put = (map, key, drug) => {
      if (!key) return;
      if (!map.has(key)) map.set(key, new Set());
      map.get(key).add(drug);
    };
    (drugs || []).forEach(drug => {
      const key = baseKey(drug.name);
      put(idx.primary, key, drug);
      derivedKeys(key).forEach(k => put(idx.derived, k, drug));
      (drug.brands || []).forEach(b => put(idx.brand, baseKey(b), drug));
    });
    return idx;
  }

  function uniqueHit(map, key) {
    const hits = map.get(key);
    return hits && hits.size === 1 ? hits.values().next().value : null;
  }

  // Exact name, salt/prefix-stripped name, synonym (resolved to the spelling this
  // index uses, e.g. aspirin -> Acetylsalicylic Acid), brand name; then the same
  // without dose/form words. No fuzzy step: returns null when unsure.
  function findExactDrug(query) {
    if (!exactIndex) return null;
    const first = baseKey(query);
    const tries = [first];
    const noDose = stripDose(first);
    if (noDose !== first) tries.push(noDose);
    for (const key of tries) {
      const keys = [key].concat(derivedKeys(key));
      for (const map of [exactIndex.primary, exactIndex.derived]) {
        for (const k of keys) { const hit = uniqueHit(map, k); if (hit) return hit; }
      }
      for (const k of keys) {
        for (const s of synonymsOf(k)) {
          for (const map of [exactIndex.primary, exactIndex.derived]) {
            const hit = uniqueHit(map, s); if (hit) return hit;
          }
        }
      }
      const hit = uniqueHit(exactIndex.brand, key);
      if (hit) return hit;
    }
    return null;
  }

  const MATCH_TEXT = {
    "exact": "名称が完全に一致",
    "only": "この名称と完全に一致する医薬品はありません。以下は名称または元の適応症の記載が近い関連結果で、同じ医薬品ではありません。開く前に確認してください：",
    "after": "その他の関連結果（同じ医薬品ではありません）：",
    "hidden": "{name}（{level}）は名称が完全に一致しますが、エビデンスレベルの絞り込みで非表示になっています。"
  };

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
  let exactIndex = null;
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
      exactIndex = buildExactIndex(data.drugs);

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
      results.innerHTML = '<div class="lookup-notice">検索インデックスを読み込めませんでした。ページを再読み込みしてください。</div>';
    });

  // 工具函數
  function getSelectedLevels() {
    return Array.from(levelFilters)
      .filter(cb => cb.checked)
      .map(cb => cb.value);
  }

  function filterByLevel(items, levels) {
    return items.filter(item => !item.level || levels.includes(item.level));
  }

  // 索引裡的分數是百分比數字（99.91）；頁面一律顯示 0–1 的模型分數，不用 %
  function formatScore(s) {
    const v = Number(s);
    if (!isFinite(v)) return '—';
    return (v > 1 ? v / 100 : v).toFixed(4);
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
      results.innerHTML = '<div class="lookup-notice">検索インデックスを読み込んでいます...</div>';
      return;
    }

    if (!query || query.length < 2) {
      if (showHint) {
        results.innerHTML = '<div class="lookup-notice">2 文字以上入力してください</div>';
      } else {
        results.innerHTML = '';
      }
      return;
    }

    const levels = getSelectedLevels();
    if (levels.length === 0 && levelFilters.length > 0) {
      results.innerHTML = '<div class="lookup-notice">エビデンスレベルを 1 つ以上選択してください</div>';
      return;
    }

    let html = '';

    // 搜尋藥物
    // Exact match first; Fuse.js results are only listed as related results and are
    // never shown as the match for the typed name. Levels without a checkbox on
    // this page (e.g. N/A) are not filtered out.
    const filterable = Array.from(levelFilters).map(cb => cb.value);
    const levelOk = lv => !filterable.includes(lv) || levels.includes(lv);
    const exactDrug = findExactDrug(query);
    const exactHidden = exactDrug && !levelOk(exactDrug.level);
    const relatedDrugs = drugFuse.search(query)
      .filter(r => r.item !== exactDrug)
      .map(r => ({ item: r.item, match: 'similar' }));
    const filteredDrugs = (exactDrug ? [{ item: exactDrug, match: 'exact' }] : [])
      .concat(relatedDrugs)
      .filter(r => levelOk(r.item.level))
      .slice(0, 5);

    if (exactHidden) {
      html += '<div class="lookup-notice" data-match="exact-hidden">' +
        MATCH_TEXT.hidden.replace('{name}', escapeHtml(exactDrug.name)).replace('{level}', escapeHtml(exactDrug.level)) + '</div>';
    }

    if (filteredDrugs.length > 0) {
      html += '<div class="result-section"><div class="section-title">該当する医薬品</div>';
      let lastMatch = null;
      filteredDrugs.forEach(r => {
        const drug = r.item;
        const brands = drug.brands && drug.brands.length > 0
          ? ' (' + drug.brands.slice(0, 2).join('、') + ')'
          : '';
        const filteredInds = filterByLevel(drug.indications || [], levels);

        if (r.match !== lastMatch) {
          const note = r.match === 'exact' ? MATCH_TEXT.exact : (exactDrug ? MATCH_TEXT.after : MATCH_TEXT.only);
          html += '<div class="match-note match-' + r.match + '" style="font-size:0.85em;color:#555;margin:0.5rem 0 0.25rem;">' + escapeHtml(note) + '</div>';
          lastMatch = r.match;
        }
        html += '<div class="result-card" data-match="' + r.match + '">';
        html += '<div class="result-header">';
        html += '<a href="' + (drug.url || config.drugsBaseUrl + drug.slug + '/') + '" class="drug-name">' + escapeHtml(drug.name) + escapeHtml(brands) + '</a>';
        html += '<span class="level-badge level-' + drug.level + '">' + drug.level + '</span>';
        html += '</div>';
        html += '<div class="result-original">元の適応症：' + (escapeHtml(drug.original) || '—') + '</div>';
        html += '<div class="result-indications"><strong>予測新規適応症：</strong>';

        if (filteredInds.length > 0) {
          filteredInds.slice(0, 5).forEach(ind => {
            html += '<span class="ind-item"><span class="level-badge level-' + ind.level + '">' + ind.level + '</span> ' + escapeHtml(ind.name) + '（スコア ' + formatScore(ind.score) + '）</span>';
          });
          if (filteredInds.length > 5) {
            html += '<span class="more">…全 ' + filteredInds.length + ' 件</span>';
          }
        } else {
          html += '<span class="no-match">（絞り込み条件に該当なし）</span>';
        }

        html += '</div>';
        html += '<a href="' + (drug.url || config.drugsBaseUrl + drug.slug + '/') + '" class="view-report">完全なレポートを見る →</a>';
        html += '</div>';
      });
      html += '</div>';
    }

    // 搜尋適應症
    const indResults = indicationFuse.search(query).slice(0, 5);
    const filteredInds = indResults.filter(r => !r.item.level || levels.includes(r.item.level));

    if (filteredInds.length > 0) {
      html += '<div class="result-section"><div class="section-title">該当する適応症</div>';
      filteredInds.forEach(r => {
        const ind = r.item;
        const indDrugs = filterByLevel(ind.drugs || [], levels);

        html += '<div class="result-card">';
        html += '<div class="result-header">';
        html += '<span class="indication-name">' + escapeHtml(ind.name) + '</span>';
        if (ind.level) html += '<span class="level-badge level-' + ind.level + '">' + ind.level + '</span>';
        html += '</div>';
        html += '<div class="result-drugs"><strong>候補医薬品（' + indDrugs.length + '）：</strong>';

        indDrugs.slice(0, 5).forEach(d => {
          html += '<div class="drug-item">';
          html += '<a href="' + (d.url || config.drugsBaseUrl + d.slug + '/') + '">' + escapeHtml(d.drug || d.name || '') + '</a>';
          if (d.level) html += '<span class="level-badge level-' + d.level + '">' + d.level + '</span>';
          html += '<span class="score">スコア ' + formatScore(d.score) + '</span>';
          if (d.original) html += '<span class="original-hint">' + escapeHtml(d.original) + '</span>';
          html += '</div>';
        });

        if (indDrugs.length > 5) {
          html += '<div class="more">…全 ' + indDrugs.length + ' 件の医薬品</div>';
        }

        html += '</div></div>';
      });
      html += '</div>';
    }

    if (!html) {
      html = '<div class="lookup-notice">該当する結果はありません</div>';
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
