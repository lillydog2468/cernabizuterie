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
  document.querySelectorAll('a[data-lightbox]').forEach((a) => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      img.src = a.getAttribute('href');
      img.alt = a.dataset.caption || '';
      cap.textContent = a.dataset.caption || '';
      dlg.showModal();
    });
  });
  dlg.addEventListener('click', (e) => {
    if (e.target === dlg) dlg.close();
  });
})();
