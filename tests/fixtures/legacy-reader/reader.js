// Every route is a deliberate choice. Hashes support reload, back and deep links.
(() => {
  const views = [...document.querySelectorAll('[data-view]')];
  function navigate() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)) || 'edition'; }
    catch { id = 'edition'; }
    const target = document.getElementById(id) || document.getElementById('edition');
    const view = target.closest('[data-view]');
    views.forEach(panel => { panel.hidden = panel !== view; });
    if (target.tagName === 'DETAILS') target.open = true;
    target.scrollIntoView({behavior:'instant', block:'start'});
    const heading = view.querySelector('h1,h2');
    if (heading) { heading.tabIndex = -1; heading.focus({preventScroll:true}); }
  }
  addEventListener('hashchange', navigate);
  navigate();
})();
