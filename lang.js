(function () {
  var STORAGE_KEY = 'cerna-lang';
  var SUPPORTED = ['cs', 'en', 'fr', 'de'];

  function detectLang() {
    var langs = [];
    if (navigator.languages && navigator.languages.length) {
      langs = navigator.languages.slice();
    } else if (navigator.language) {
      langs = [navigator.language];
    }
    for (var i = 0; i < langs.length; i++) {
      var code = String(langs[i] || '').toLowerCase();
      var primary = code.split('-')[0];
      if (primary === 'cs' || primary === 'sk') return 'cs';
      if (primary === 'en') return 'en';
      if (primary === 'fr') return 'fr';
      if (primary === 'de') return 'de';
    }
    return 'en';
  }

  function getPreferredLang() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved && SUPPORTED.indexOf(saved) !== -1) return saved;
    } catch (e) {}
    return detectLang();
  }

  function setLang(lang) {
    if (SUPPORTED.indexOf(lang) === -1) return;
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
  }

  /** Root redirector: /index.html → /{lang}/index.html (relative — works on GitHub Pages) */
  function redirectRoot() {
    var lang = getPreferredLang();
    location.replace(lang + '/index.html');
  }

  function initSwitcher() {
    var links = document.querySelectorAll('.lang-switch a[data-lang]');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function () {
        setLang(this.getAttribute('data-lang'));
      });
    }
  }

  window.CernaLang = {
    detectLang: detectLang,
    getPreferredLang: getPreferredLang,
    setLang: setLang,
    redirectRoot: redirectRoot,
    initSwitcher: initSwitcher,
    STORAGE_KEY: STORAGE_KEY,
    SUPPORTED: SUPPORTED
  };

  if (document.documentElement.getAttribute('data-cerna-redirect') === '1') {
    redirectRoot();
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSwitcher);
  } else {
    initSwitcher();
  }
})();
