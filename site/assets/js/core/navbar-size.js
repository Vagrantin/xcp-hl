// Hextra's sidebar/TOC offsets assume one 4rem navbar row. Wrapping at narrow
// widths or with enlarged text needs the actual height, including font changes.
(function () {
  const navbar = document.querySelector('nav.hextra-max-navbar-width');
  if (!navbar) return;
  function syncHeight() {
    const height = navbar.getBoundingClientRect().height;
    document.documentElement.style.setProperty('--navbar-height', `${height}px`);
    // A wrapped navbar can grow after the browser initially positions a hash
    // target (for example while fonts load). Correct a heading still visible
    // beneath the bar; do not jump back to a heading the reader has passed.
    let target;
    try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); }
    catch (_) { return; }
    const heading = target?.closest('h2, h3, h4, h5, h6');
    if (heading) {
      const top = heading.getBoundingClientRect().top;
      if (top >= 0 && top < height) heading.scrollIntoView({block: 'start'});
    }
  }
  syncHeight();
  if (typeof ResizeObserver !== 'undefined') {
    new ResizeObserver(syncHeight).observe(navbar);
  } else {
    window.addEventListener('resize', syncHeight);
  }
})();
