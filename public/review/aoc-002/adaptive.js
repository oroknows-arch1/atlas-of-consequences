
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


  const routes = [...document.querySelectorAll('.perspective-route')];
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
  const playButton = document.createElement('button');
  playButton.type = 'button';
  playButton.className = 'opening-play-button';
  playButton.textContent = 'Play cinematic opening';
  playButton.setAttribute('aria-label', 'Play silent cinematic opening');
  playButton.style.cssText = 'position:absolute;z-index:7;left:50%;bottom:max(36px,env(safe-area-inset-bottom));transform:translateX(-50%);padding:14px 22px;background:rgba(5,7,8,.85);color:#fff;border:1px solid #fff;border-radius:999px;font:600 13px Arial,sans-serif;cursor:pointer;white-space:nowrap;';
  hero.appendChild(playButton);
  const reveal = () => {
    hero.classList.add('film-complete');
    playButton.hidden = true;
    playButton.style.display = 'none';
  };
  const showPlay = (label = 'Play cinematic opening') => {
    if (hero.classList.contains('film-complete')) return;
    playButton.textContent = label;
    playButton.hidden = false;
    playButton.style.display = 'block';
  };
  const playOpening = async () => {
    if (!video) { showPlay('Opening video unavailable · Skip opening'); return; }
    video.muted = true;
    video.defaultMuted = true;
    video.volume = 0;
    video.playsInline = true;
    try {
      await video.play();
      playButton.hidden = true;
      playButton.style.display = 'none';
      hero.classList.remove('tap-to-play');
    } catch (_) {
      showPlay('Tap to play cinematic opening');
    }
  };
  playButton.addEventListener('click', event => {
    event.stopPropagation();
    if (video && video.error) { reveal(); return; }
    playOpening();
  });
  video?.addEventListener('ended', reveal, { once: true });
  skip?.addEventListener('click', event => {
    event.stopPropagation();
    video?.pause();
    reveal();
  });
  video?.addEventListener('error', () => {
    showPlay('Video unavailable · Skip opening');
    playButton.disabled = true;
    playButton.style.opacity = '.65';
  });
  video?.addEventListener('playing', () => {
    playButton.hidden = true;
    playButton.style.display = 'none';
  });
  // Some browsers do not dispatch a useful error when a video source is empty.
  video?.addEventListener('stalled', () => showPlay('Tap to play cinematic opening'));
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Leave the user in control of the film; do not discard the opening.
    showPlay();
  } else {
    playOpening();
  }
  hero.addEventListener('click', event => {
    if (event.target.closest('a,button')) return;
    if (video?.paused && !hero.classList.contains('film-complete')) playOpening();
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

// Owner audio lock: AOC-002 must remain silent with no playback controls.
(() => {
  const video = document.querySelector('.hero-video');
  if (!video) return;
  const enforceSilence = () => { video.defaultMuted = true; video.muted = true; video.volume = 0; video.removeAttribute('controls'); };
  enforceSilence();
  video.addEventListener('volumechange', enforceSilence);
  video.addEventListener('loadedmetadata', enforceSilence);
})();

// Keep review links on current authoritative NUPRC document indexes when
// the regulator retires direct PDF paths.
(() => {
  const replacements = new Map([
    ['https://www.nuprc.gov.ng/wp-content/uploads/2022/07/Nigeria-Upstream-Petroleum-Host-Communities-Development-Regulations-2022.pdf', 'https://www.nuprc.gov.ng/laws/regulations/gazetted'],
    ['https://br2025.nuprc.gov.ng/media/ggwk4wxe/petroleum-industry-act-2021.pdf', 'https://www.nuprc.gov.ng/laws/acts/petroleum-industry-act'],
    ['https://www.nuprc.gov.ng/wp-content/uploads/2022/12/Gas-Flaring-and-Venting-Regulations-2022-D.pdf', 'https://www.nuprc.gov.ng/laws/regulations/gazetted'],
  ]);
  document.querySelectorAll('a[href]').forEach(link => {
    const replacement = replacements.get(link.href);
    if (replacement) link.href = replacement;
  });
})();
