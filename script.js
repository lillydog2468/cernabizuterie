(function () {
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
