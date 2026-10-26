(function () {
  const interestLocations = {
    'index.html': 'home',
    'vyrobky.html': 'products',
    'ceny.html': 'prices',
    'historie.html': 'history',
    'sklo.html': 'glass',
    'kontakt.html': 'contact',
    'oceneni.html': 'awards',
    'o-stanislavovi.html': 'about',
    'about-stanislav.html': 'about',
    'a-propos-de-stanislav.html': 'about',
    'ueber-stanislav.html': 'about'
  };

  document.querySelectorAll('.interest-entry a').forEach((link) => {
    link.addEventListener('click', () => {
      if (typeof gtag !== 'function') return;
      const parts = location.pathname.split('/').filter(Boolean);
      const folder = parts[0] || '';
      const pageLanguage = (folder === 'cs' || folder === 'en' || folder === 'fr' || folder === 'de') ? folder : 'en';
      const file = parts[parts.length - 1] || '';
      const linkLocation = interestLocations[file] || (folder === file ? 'home' : 'content');
      gtag('event', 'interest_link_click', {
        link_location: linkLocation,
        page_language: pageLanguage
      });
    });
  });

  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('site-nav');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  const dlg = document.getElementById('lightbox');
  if (!dlg) return;
  const img = document.getElementById('lb-img');
  const cap = document.getElementById('lb-cap');
  let scrollY = 0;

  function lockScroll() {
    scrollY = window.scrollY || window.pageYOffset || 0;
    document.documentElement.style.scrollBehavior = 'auto';
    document.body.style.position = 'fixed';
    document.body.style.top = '-' + scrollY + 'px';
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.width = '100%';
  }

  function unlockScroll() {
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    document.body.style.width = '';
    window.scrollTo(0, scrollY);
    // Restore smooth scrolling after the jump is settled
    requestAnimationFrame(function () {
      document.documentElement.style.scrollBehavior = '';
    });
  }

  document.querySelectorAll('a[data-lightbox]').forEach((a) => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      img.src = a.getAttribute('href');
      img.alt = a.dataset.caption || '';
      cap.textContent = a.dataset.caption || '';
      lockScroll();
      dlg.showModal();
      // Belt-and-braces: some browsers nudge scroll when focusing the dialog
      window.scrollTo(0, scrollY);
    });
  });

  dlg.addEventListener('click', (e) => {
    if (e.target === dlg) dlg.close();
  });
  dlg.addEventListener('close', unlockScroll);
})();
