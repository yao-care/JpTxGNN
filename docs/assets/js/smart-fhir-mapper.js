/**
 * SMART on FHIR Drug Mapper
 *
 * Maps medications from FHIR MedicationRequest/MedicationStatement
 * to TwTxGNN drug database using RxNorm API and fuzzy matching.
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

  // Synonym mappings (from drugbank_mapper.py)
  const SYNONYM_MAP = {
    'NIACINAMIDE': 'NICOTINAMIDE',
    'NICOTINIC ACID': 'NIACIN',
    'PYRIDOXINE': 'VITAMIN B6',
    'THIAMINE': 'VITAMIN B1',
    'RIBOFLAVIN': 'VITAMIN B2',
    'CYANOCOBALAMIN': 'VITAMIN B12',
    'ASCORBIC ACID': 'VITAMIN C',
    'TOCOPHEROL': 'VITAMIN E',
    'RETINOL': 'VITAMIN A',
    'CHOLECALCIFEROL': 'VITAMIN D3',
    'ERGOCALCIFEROL': 'VITAMIN D2',
    'PHYTONADIONE': 'VITAMIN K1',
    'ACETYLSALICYLIC ACID': 'ASPIRIN',
    'PARACETAMOL': 'ACETAMINOPHEN',
    'ADRENALINE': 'EPINEPHRINE',
    'NORADRENALINE': 'NOREPINEPHRINE',
    'LIGNOCAINE': 'LIDOCAINE',
    'FRUSEMIDE': 'FUROSEMIDE',
    'SALBUTAMOL': 'ALBUTEROL',
    'L-MENTHOL': 'LEVOMENTHOL',
    'MENTHOL': 'LEVOMENTHOL',
    'DL-MENTHOL': 'RACEMENTHOL',
    'L-ADRENALINE': 'EPINEPHRINE',
    'CAFFEINE ANHYDROUS': 'CAFFEINE',
    'DEXTROSE MONOHYDRATE': 'GLUCOSE',
    'DEXTROSE': 'GLUCOSE',
    'GLUCOSE MONOHYDRATE': 'GLUCOSE'
  };

  /**
   * DrugMapper class for mapping FHIR medications to TwTxGNN
   */
  class DrugMapper {
    constructor(searchIndex) {
      this.searchIndex = searchIndex;
      this.rxnormCache = new Map();
      this.fuseInstance = null;

      // Initialize Fuse.js if available
      if (typeof Fuse !== 'undefined' && searchIndex && searchIndex.drugs) {
        this.fuseInstance = new Fuse(searchIndex.drugs, {
          keys: ['name', 'brands'],
          threshold: 0.3,
          includeScore: true
        });
      }
    }

    /**
     * Normalize drug name by removing salts, prefixes, and applying synonyms
     * @param {string} name - Drug name to normalize
     * @returns {string} - Normalized name
     */
    normalize(name) {
      if (!name) return '';

      let normalized = name.toUpperCase().trim();

      // Remove salt suffixes
      for (const suffix of SALT_SUFFIXES) {
        if (normalized.endsWith(suffix)) {
          normalized = normalized.slice(0, -suffix.length).trim();
          break; // Only remove one suffix
        }
      }

      // Remove L-/D-/DL- prefixes
      normalized = normalized.replace(/^(L-|D-|DL-)/, '');

      // Remove parenthetical content
      normalized = normalized.replace(/\s*\([^)]*\)/g, '').trim();

      // Apply synonym mapping
      if (SYNONYM_MAP[normalized]) {
        normalized = SYNONYM_MAP[normalized];
      }

      return normalized;
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
        console.error(`Error querying RxNorm for ${rxcui}:`, error);
        return null;
      }
    }

    /**
     * Search TwTxGNN database for matching drug
     * @param {string} name - Drug name to search
     * @returns {Object|null} - Matching drug or null
     */
    searchTwTxGNN(name) {
      if (!name || !this.fuseInstance) return null;

      const normalized = this.normalize(name);
      const results = this.fuseInstance.search(normalized);

      if (results.length > 0 && results[0].score < 0.4) {
        return results[0].item;
      }

      // Also try original name
      const originalResults = this.fuseInstance.search(name);
      if (originalResults.length > 0 && originalResults[0].score < 0.4) {
        return originalResults[0].item;
      }

      return null;
    }

    /**
     * Map a single FHIR medication to TwTxGNN
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
        twtxgnnMatch: null,
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

      // Step 5: Search TwTxGNN database
      if (nameToSearch) {
        result.twtxgnnMatch = this.searchTwTxGNN(nameToSearch);
        result.matched = result.twtxgnnMatch !== null;
      }

      return result;
    }

    /**
     * Map multiple FHIR medications to TwTxGNN
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
  global.TwTxGNN = global.TwTxGNN || {};
  global.TwTxGNN.DrugMapper = DrugMapper;

})(typeof window !== 'undefined' ? window : this);
