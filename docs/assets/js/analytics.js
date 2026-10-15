/* TxGNN GA4 measurement layer（由 TwTxGNN 版泛化，母專案 .claude/add_ga4.py 產生）.
 * Keep this site connected to the shared yao.care Property without sending
 * search terms, form contents, patient data, or query strings.
 */
(function () {
  'use strict';

  var config = window.TXGNN_ANALYTICS;
  if (!config || !config.measurementId) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () {
    window.dataLayer.push(arguments);
  };
  var gtag = window.gtag;
  var linkerDomains = Array.isArray(config.linkerDomains) ? config.linkerDomains : [];
  var contentGroup = config.contentGroup || 'TxGNN';

  var aiHosts = [
    'chatgpt.com', 'chat.openai.com', 'openai.com', 'perplexity.ai',
    'gemini.google.com', 'copilot.microsoft.com', 'claude.ai', 'grok.com',
    'poe.com', 'you.com', 'phind.com', 'felo.ai', 'genspark.ai',
    'deepseek.com', 'kimi.moonshot.cn', 'doubao.com'
  ];
  var searchHosts = [
    'google.', 'bing.com', 'search.yahoo.com', 'duckduckgo.com', 'yandex.',
    'baidu.com', 'naver.com'
  ];
  var socialHosts = [
    'facebook.com', 'instagram.com', 'linkedin.com', 'x.com', 'twitter.com',
    'youtube.com', 'line.me'
  ];
  var citationHosts = [
    'pubmed.ncbi.nlm.nih.gov', 'clinicaltrials.gov', 'doi.org', 'nature.com',
    'zitniklab.hms.harvard.edu', 'dataverse.harvard.edu',
    'zenodo.org', 'github.com', 'drugbank.com'
  ].concat(Array.isArray(config.citationHosts) ? config.citationHosts : []);
  var crossSiteHosts = [
    'yao.care', 'www.yao.care', 'www.ods.yao.care', 'app.ods.yao.care'
  ];

  function hostMatches(host, candidates) {
    return candidates.some(function (candidate) {
      return host === candidate || host.endsWith('.' + candidate) || host.indexOf(candidate) !== -1;
    });
  }

  function referrerHost() {
    if (!document.referrer) return '';
    try {
      return new URL(document.referrer).hostname.toLowerCase();
    } catch (_) {
      return '';
    }
  }

  function classifyTraffic(host) {
    if (!host) return { category: 'direct' };
    if (host === window.location.hostname) return { category: 'internal' };
    var aiSource = aiHosts.find(function (candidate) { return hostMatches(host, [candidate]); });
    if (aiSource) return { category: 'ai', aiSource: aiSource };
    if (hostMatches(host, searchHosts)) return { category: 'search' };
    if (hostMatches(host, socialHosts)) return { category: 'social' };
    return { category: 'referral' };
  }

  function cleanPath(value) {
    try {
      return new URL(value, window.location.href).pathname || '/';
    } catch (_) {
      return '/';
    }
  }

  var traffic = classifyTraffic(referrerHost());
  var pageType = config.pageType || 'reference';
  var pagePath = cleanPath(config.pagePath || window.location.pathname);
  var pageCategory = {
    home: 'home',
    drug_report: 'drug_report',
    news: 'news',
    smart: 'smart_on_fhir',
    reference: 'research_reference'
  }[pageType] || 'research_reference';
  var baseEventParams = {
    content_group: contentGroup,
    content_type: pageType,
    content_category: pageCategory,
    content_item: pagePath,
    page_evidence_level: config.pageEvidenceLevel || undefined,
    traffic_category: traffic.category
  };
  if (traffic.aiSource) baseEventParams.ai_source = traffic.aiSource;

  gtag('js', new Date());
  gtag('set', 'linker', { domains: linkerDomains, accept_incoming: true });
  gtag('config', config.measurementId, {
    linker: { domains: linkerDomains, accept_incoming: true },
    content_group: contentGroup,
    content_type: pageType,
    content_category: pageCategory,
    content_item: pagePath,
    page_location: window.location.origin + pagePath,
    page_title: config.pageTitle || document.title,
    page_language: config.language || document.documentElement.lang || undefined,
    traffic_category: traffic.category,
    ai_source: traffic.aiSource || undefined
  });

  function track(eventName, params) {
    var eventParams = Object.assign({}, baseEventParams, params || {});
    Object.keys(eventParams).forEach(function (key) {
      if (eventParams[key] === undefined || eventParams[key] === null || eventParams[key] === '') {
        delete eventParams[key];
      }
    });
    gtag('event', eventName, eventParams);
  }

  window.txgnnTrack = track;

  var milestones = [25, 50, 75, 100];
  var reached = {};
  function reportScrollDepth() {
    var scrollable = document.documentElement.scrollHeight - window.innerHeight;
    if (scrollable < 200) return;
    var depth = Math.min(100, Math.round((window.scrollY / scrollable) * 100));
    milestones.forEach(function (milestone) {
      if (depth >= milestone && !reached[milestone]) {
        reached[milestone] = true;
        track('scroll_depth', { percent_scrolled: milestone });
        if (milestone === 100) track('read_complete', { completion: 'scroll_100' });
      }
    });
  }
  window.addEventListener('scroll', reportScrollDepth, { passive: true });

  [30, 60, 120].forEach(function (seconds) {
    window.setTimeout(function () {
      track('page_engagement', { elapsed_seconds: seconds });
    }, seconds * 1000);
  });

  function linkInfo(anchor) {
    var href = anchor.getAttribute('href');
    if (!href) return null;
    try {
      var url = new URL(href, window.location.href);
      if (url.protocol !== 'http:' && url.protocol !== 'https:') return { protocol: url.protocol };
      return {
        host: url.hostname.toLowerCase(),
        path: url.pathname || '/',
        sameOrigin: url.origin === window.location.origin
      };
    } catch (_) {
      return null;
    }
  }

  document.addEventListener('click', function (event) {
    var anchor = event.target instanceof Element ? event.target.closest('a') : null;
    if (!anchor) return;
    var info = linkInfo(anchor);
    if (!info) return;

    if (info.protocol === 'mailto:') {
      track('contact_click', { cta_type: 'email' });
      return;
    }
    if (anchor.classList.contains('drug-name')) {
      track('report_open', { report_path: info.path });
      return;
    }
    if (crossSiteHosts.indexOf(info.host) !== -1) {
      track('cta_click', { cta_type: 'cross_site', destination_host: info.host, destination_path: info.path });
      return;
    }
    if (hostMatches(info.host, citationHosts)) {
      track('citation_click', { citation_host: info.host, citation_path: info.path });
    }
  });

  function wireLookup() {
    var input = document.getElementById('lookup-input');
    var submit = document.getElementById('lookup-search');
    if (!input || !submit) return;
    var submitSearch = function () {
      var length = (input.value || '').trim().length;
      track('search_submit', {
        search_surface: 'drug_lookup',
        query_length: Math.min(length, 100)
      });
    };
    submit.addEventListener('click', submitSearch);
    input.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') submitSearch();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireLookup);
  } else {
    wireLookup();
  }
})();
