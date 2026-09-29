
(() => {
  const params = new URLSearchParams(location.search);
  const incomingPerspective = params.get('perspective');
  if (incomingPerspective) {
    const card = document.querySelector('[data-perspective="' + CSS.escape(incomingPerspective) + '"]');
    if (card) {
      card.classList.add('incoming-perspective');
      const marker = document.createElement('span');
      marker.className = 'incoming-marker';
      marker.textContent = 'CONNECTED TO WHAT BROUGHT YOU HERE';
      const markerHost = card.querySelector('div');
      if (markerHost) markerHost.prepend(marker);
      else card.setAttribute('aria-description', marker.textContent);
    }
  }


  const routes = [...document.querySelectorAll('.route')];
  const closeRoutes = () => routes.forEach(route => { route.hidden = true; });
  const openRoute = (perspective) => {
    const route = routes.find(item => item.dataset.route === perspective);
    if (!route) return false;
    closeRoutes();
    route.hidden = false;
    return true;
  };
  document.querySelectorAll('[data-perspective][href]').forEach(entry => {
    entry.addEventListener('click', () => openRoute(entry.dataset.perspective));
  });
  document.querySelectorAll('.route-exit, .route header a[href="#perspectives"]').forEach(exitLink => {
    exitLink.addEventListener('click', () => closeRoutes());
  });

  const hero = document.querySelector('.video-entry');
  const video = document.querySelector('.hero-video');
  if (!hero) return;
  const skip = hero.querySelector('.skip-film');
  const reveal = () => {
    hero.classList.add('film-complete');
    try { if (video) video.currentTime = Math.max(0, video.duration - 0.05); } catch (_) {}
  };
  video?.addEventListener('ended', reveal, { once:true });
  skip?.addEventListener('click', (event) => {
    event.stopPropagation();
    video?.pause();
    reveal();
  });
  video?.addEventListener('error', reveal, { once:true });
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) reveal();
  else if (video) video.play().catch(() => hero.classList.add('tap-to-play'));
  else setTimeout(reveal, 6000);
  hero.addEventListener('click', () => {
    if (hero.classList.contains('tap-to-play') && video?.paused) {
      video?.play().then(() => hero.classList.remove('tap-to-play')).catch(reveal);
    }
  });
  // Edition routing extends canonical click behaviour to reload, Back and source anchors.
  const navigate = () => {
    let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { id = ''; }
    const destination = document.getElementById(id);
    const route = destination?.closest('.route');
    closeRoutes();
    if (route) { route.hidden = false; if (destination.tagName === 'DETAILS') destination.open = true; route.scrollIntoView(); }
    else if (destination) destination.scrollIntoView();
  };
  addEventListener('hashchange', navigate);
  navigate();
})();
