/**
 * SMART on FHIR Drug Mapper
 *
 * Maps medications from FHIR MedicationRequest/MedicationStatement
 * to JpTxGNN drug database using RxNorm API, exact/synonym name matching
 * and a strict fuzzy fallback (returns "not found" rather than a different drug).
 */
(function(global) {
  'use strict';

  // Salt suffixes to remove for normalization (from drugbank_mapper.py)
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

  // Fuzzy fallback (typos / language endings such as METFORMINA, OMEPRAZOL).
  // Fuse.js only proposes candidates; a candidate is accepted only if it
  // passes isSafeFuzzyMatch(). Anything else is reported as "not found".
  const FUSE_THRESHOLD = 0.2;
  const FUZZY_MIN_TOKEN_LENGTH = 6;
  const FUZZY_SAME_PREFIX = 4;

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

  function editDistance(a, b) {
    if (Math.abs(a.length - b.length) > 1) return 2;
    let prev = Array.from({ length: b.length + 1 }, (_, j) => j);
    for (let i = 1; i <= a.length; i++) {
      const cur = [i];
      for (let j = 1; j <= b.length; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      }
      prev = cur;
    }
    return prev[b.length];
  }

  // Accept a fuzzy match only when the two names have the same words except
  // one, and that word differs by a single edit after the first 4 letters,
  // has no digits and is at least 6 letters long. This rejects pairs such as
  // ACLIDINIUM/CLIDINIUM, POTASSIUM CITRATE/NITRATE, VITAMIN A/D,
  // INTERFERON BETA-1A/1B, PREDNISONE/PREDNISOLONE, CITALOPRAM/ESCITALOPRAM.
  function isSafeFuzzyMatch(query, candidate) {
    const qa = query.split(' ');
    const ca = candidate.split(' ');
    if (qa.length !== ca.length) return false;
    let diff = -1;
    for (let i = 0; i < qa.length; i++) {
      if (qa[i] !== ca[i]) {
        if (diff !== -1) return false;
        diff = i;
      }
    }
    if (diff === -1) return true;
    const q = qa[diff];
    const c = ca[diff];
    if (/\d/.test(q) || /\d/.test(c)) return false;
    if (Math.min(q.length, c.length) < FUZZY_MIN_TOKEN_LENGTH) return false;
    if (q.slice(0, FUZZY_SAME_PREFIX) !== c.slice(0, FUZZY_SAME_PREFIX)) return false;
    return editDistance(q, c) <= 1;
  }

  /**
   * DrugMapper class for mapping FHIR medications to JpTxGNN
   */
  class DrugMapper {
    constructor(searchIndex) {
      this.searchIndex = searchIndex;
      this.rxnormCache = new Map();
      this.fuseInstance = null;

      const drugs = (searchIndex && searchIndex.drugs) || [];
      this.drugs = drugs;
      // Lookup tables: exact names first, then salt/prefix-stripped names,
      // then brand names. A key shared by two different drugs is ambiguous
      // and never used.
      this.primaryIndex = new Map();
      this.derivedIndex = new Map();
      this.brandIndex = new Map();
      const put = (map, key, drug) => {
        if (!key) return;
        if (!map.has(key)) map.set(key, new Set());
        map.get(key).add(drug);
      };
      for (const drug of drugs) {
        const key = baseKey(drug.name);
        put(this.primaryIndex, key, drug);
        for (const k of derivedKeys(key)) put(this.derivedIndex, k, drug);
        for (const brand of (drug.brands || [])) put(this.brandIndex, baseKey(brand), drug);
      }

      // Fuse.js is only a candidate generator for the strict fuzzy fallback.
      if (typeof Fuse !== 'undefined' && drugs.length) {
        this.fuseInstance = new Fuse(drugs, {
          keys: ['name'],
          threshold: FUSE_THRESHOLD,
          ignoreLocation: true,
          includeScore: true
        });
      }
    }

    /**
     * Normalize drug name: upper-case, strip accents, salt suffix and
     * L-/D-/DL- prefix, then map to this site's spelling when a synonym of
     * it is in the search index.
     * @param {string} name - Drug name to normalize
     * @returns {string} - Normalized name
     */
    normalize(name) {
      const key = baseKey(name);
      if (!key) return '';
      const derived = derivedKeys(key);
      const stem = derived.length ? derived[derived.length - 1] : key;
      for (const k of [key, ...derived]) {
        if (this.primaryIndex && this.primaryIndex.has(k)) return k;
        for (const syn of synonymsOf(k)) {
          if (this.primaryIndex && this.primaryIndex.has(syn)) return syn;
        }
      }
      return stem;
    }

    lookupKey(map, key) {
      const hits = map.get(key);
      return hits && hits.size === 1 ? hits.values().next().value : null;
    }

    findExact(key) {
      const keys = [key, ...derivedKeys(key)];
      for (const map of [this.primaryIndex, this.derivedIndex]) {
        for (const k of keys) {
          const hit = this.lookupKey(map, k);
          if (hit) return hit;
        }
      }
      for (const k of keys) {
        for (const syn of synonymsOf(k)) {
          for (const map of [this.primaryIndex, this.derivedIndex]) {
            const hit = this.lookupKey(map, syn);
            if (hit) return hit;
          }
        }
      }
      return this.lookupKey(this.brandIndex, key);
    }

    findFuzzy(key) {
      const queries = [key, stripSalt(key)].filter((k, i, a) => k && a.indexOf(k) === i);
      let candidates = this.drugs;
      if (this.fuseInstance) {
        candidates = [];
        for (const q of queries) {
          for (const r of this.fuseInstance.search(q)) {
            if (r.score <= FUSE_THRESHOLD && !candidates.includes(r.item)) candidates.push(r.item);
          }
        }
      }
      const accepted = new Set();
      for (const drug of candidates) {
        const name = baseKey(drug.name);
        const names = [name, stripSalt(name)];
        if (queries.some(q => names.some(n => isSafeFuzzyMatch(q, n)))) accepted.add(drug);
      }
      // Two different drugs both "close enough" means we cannot tell: not found.
      return accepted.size === 1 ? accepted.values().next().value : null;
    }

    /**
     * Find the drug for a name in this site's search index.
     * Order: exact name, salt/prefix-stripped name, synonym, brand name,
     * the same after dropping dose/form words, then a strict fuzzy match.
     * Returns null rather than a different drug when unsure.
     * @param {string} name - Drug name to search
     * @returns {Object|null} - Matching drug or null
     */
    findDrug(name) {
      const key = baseKey(name);
      if (!key || !this.drugs.length) return null;
      const keys = [key];
      const noDose = stripDose(key);
      if (noDose !== key) keys.push(noDose);
      for (const k of keys) {
        const hit = this.findExact(k);
        if (hit) return hit;
      }
      for (const k of keys) {
        const hit = this.findFuzzy(k);
        if (hit) return hit;
      }
      return null;
    }

    /**
     * Extract RxCUI from FHIR medication coding
     * @param {Object} medication - FHIR medication resource or codeable concept
     * @returns {string|null} - RxCUI or null
     */
    extractRxCui(medication) {
      const codings = medication?.medicationCodeableConcept?.coding ||
                      medication?.code?.coding ||
                      medication?.coding ||
                      [];

      for (const coding of codings) {
        // RxNorm system URIs
        if (coding.system === 'http://www.nlm.nih.gov/research/umls/rxnorm' ||
            coding.system === 'urn:oid:2.16.840.1.113883.6.88') {
          return coding.code;
        }
      }

      return null;
    }

    /**
     * Extract display name from FHIR medication
     * @param {Object} medication - FHIR medication resource
     * @returns {string|null} - Display name or null
     */
    extractDisplayName(medication) {
      const codings = medication?.medicationCodeableConcept?.coding ||
                      medication?.code?.coding ||
                      medication?.coding ||
                      [];

      for (const coding of codings) {
        if (coding.display) {
          return coding.display;
        }
      }

      return medication?.medicationCodeableConcept?.text ||
             medication?.code?.text ||
             medication?.text ||
             null;
    }

    /**
     * Query RxNorm API to get ingredient name from RxCUI
     * @param {string} rxcui - RxNorm concept identifier
     * @returns {Promise<string|null>} - Ingredient name or null
     */
    async getRxNormIngredient(rxcui) {
      if (!rxcui) return null;

      // Check cache
      if (this.rxnormCache.has(rxcui)) {
        return this.rxnormCache.get(rxcui);
      }

      try {
        // NLM RxNav API - get related ingredients
        const url = `https://rxnav.nlm.nih.gov/REST/rxcui/${rxcui}/related.json?tty=IN`;
        const response = await fetch(url);

        if (!response.ok) {
          console.warn(`RxNorm API error for ${rxcui}: ${response.status}`);
          return null;
        }

        const data = await response.json();

        // Extract ingredient name from response
        const conceptGroup = data?.relatedGroup?.conceptGroup;
        if (conceptGroup && conceptGroup.length > 0) {
          const conceptProps = conceptGroup[0]?.conceptProperties;
          if (conceptProps && conceptProps.length > 0) {
            const ingredientName = conceptProps[0].name;
            this.rxnormCache.set(rxcui, ingredientName);
            return ingredientName;
          }
        }

        // Try alternative: get properties directly
        const propUrl = `https://rxnav.nlm.nih.gov/REST/rxcui/${rxcui}/properties.json`;
        const propResponse = await fetch(propUrl);

        if (propResponse.ok) {
          const propData = await propResponse.json();
          const name = propData?.properties?.name;
          if (name) {
            this.rxnormCache.set(rxcui, name);
            return name;
          }
        }

        this.rxnormCache.set(rxcui, null);
        return null;

      } catch (error) {
        console.error('Error querying RxNorm for %s:', rxcui, error);
        return null;
      }
    }

    /**
     * Search JpTxGNN database for matching drug
     * @param {string} name - Drug name to search
     * @returns {Object|null} - Matching drug or null
     */
    searchJpTxGNN(name) {
      return this.findDrug(name);
    }

    /**
     * Map a single FHIR medication to JpTxGNN
     * @param {Object} medication - FHIR MedicationRequest or MedicationStatement
     * @returns {Promise<Object>} - Mapping result
     */
    async mapMedication(medication) {
      const result = {
        fhirResource: medication,
        rxcui: null,
        displayName: null,
        ingredientName: null,
        normalizedName: null,
        jptxgnnMatch: null,
        matched: false
      };

      // Step 1: Extract display name
      result.displayName = this.extractDisplayName(medication);

      // Step 2: Extract RxCUI
      result.rxcui = this.extractRxCui(medication);

      // Step 3: Get ingredient name from RxNorm
      if (result.rxcui) {
        result.ingredientName = await this.getRxNormIngredient(result.rxcui);
      }

      // Step 4: Normalize the best available name
      const nameToSearch = result.ingredientName || result.displayName;
      if (nameToSearch) {
        result.normalizedName = this.normalize(nameToSearch);
      }

      // Step 5: Search JpTxGNN database
      if (nameToSearch) {
        result.jptxgnnMatch = this.searchJpTxGNN(nameToSearch);
        result.matched = result.jptxgnnMatch !== null;
      }

      return result;
    }

    /**
     * Map multiple FHIR medications to JpTxGNN
     * @param {Array} medications - Array of FHIR medication resources
     * @returns {Promise<Array>} - Array of mapping results
     */
    async mapMedications(medications) {
      const results = [];

      for (const med of medications) {
        const result = await this.mapMedication(med);
        results.push(result);
      }

      return results;
    }

    /**
     * Extract medications from FHIR Bundle
     * @param {Object} bundle - FHIR Bundle resource
     * @returns {Array} - Array of medication resources
     */
    extractFromBundle(bundle) {
      if (!bundle || !bundle.entry) return [];

      return bundle.entry
        .filter(entry => {
          const type = entry.resource?.resourceType;
          return type === 'MedicationRequest' ||
                 type === 'MedicationStatement' ||
                 type === 'Medication';
        })
        .map(entry => entry.resource);
    }
  }

  // Export to global scope
  global.JpTxGNN = global.JpTxGNN || {};
  global.JpTxGNN.DrugMapper = DrugMapper;

})(typeof window !== 'undefined' ? window : this);
