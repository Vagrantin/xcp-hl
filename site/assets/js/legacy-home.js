// Preserve old Jekyll homepage deep links after the guide moved to /docs/start/.
(() => {
  function redirectLegacyFragment() {
    let id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch { return; }
    if (!id) return;
    const target = document.getElementById(id);
    if (target && target.classList.contains('legacy-home-anchor')) {
      const link = target.querySelector('a');
      if (link) window.location.replace(link.href);
    }
  }
  window.addEventListener('hashchange', redirectLegacyFragment);
  redirectLegacyFragment();
})();
