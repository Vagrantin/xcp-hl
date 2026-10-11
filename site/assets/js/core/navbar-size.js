// Hextra's sidebar/TOC offsets assume one 4rem navbar row. Wrapping at narrow
// widths or with enlarged text needs the actual height, including font changes.
(function () {
  const navbar = document.querySelector('nav.hextra-max-navbar-width');
  if (!navbar) return;
  function syncHeight() {
    document.documentElement.style.setProperty('--navbar-height', `${navbar.getBoundingClientRect().height}px`);
  }
  syncHeight();
  if (typeof ResizeObserver !== 'undefined') {
    new ResizeObserver(syncHeight).observe(navbar);
  } else {
    window.addEventListener('resize', syncHeight);
  }
})();
