const opening = document.querySelector('#openingSequence');

if (opening) {
  const stages = [...opening.querySelectorAll('.opening-stage')];
  const stageLabel = opening.querySelector('#openingStageLabel');
  const credit = opening.querySelector('#openingCredit');
  const progress = opening.querySelector('#openingAssetProgress');
  const enter = opening.querySelector('#openingEnter');

  const meta = [
    {
      label: 'REAL · DATA CENTRE',
      credit: 'Rsparks3 · Wikimedia Commons · CC0 1.0',
      url: 'https://commons.wikimedia.org/wiki/File:Data_center_roof.jpg'
    },
    {
      label: 'REAL · GRID / ENERGY',
      credit: 'ShootingStarMax · Wikimedia Commons · CC BY-SA 4.0',
      url: 'https://commons.wikimedia.org/wiki/File:L%C3%ADneas_alta_tensi%C3%B3n_Chile.jpg'
    },
    {
      label: 'REAL · COPPER / MINING',
      credit: 'Diego Delso, delso.photo, License CC BY-SA 4.0',
      url: 'https://commons.wikimedia.org/wiki/File:Mina_de_Chuquicamata,_Calama,_Chile,_2016-02-01,_DD_110-112_PAN.JPG'
    },
    {
      label: 'REAL · CALAMA',
      credit: 'Chris Hunkeler · Wikimedia Commons · CC BY-SA 2.0',
      url: 'https://commons.wikimedia.org/wiki/File:Homes_in_Calama,_Chile_(45418686415).jpg'
    },
    {
      label: 'STORY · FICTION',
      credit: 'Generated for AOC-001 · fictional people',
      url: null
    }
  ];

  const duration = 12500;
  const segment = 1 / (stages.length - 1);
  let startTime = null;
  let finished = false;

  function setMeta(index) {
    const item = meta[index];
    stageLabel.textContent = item.label;
    credit.innerHTML = item.url
      ? `<a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.credit}</a>`
      : item.credit;
  }

  function draw(t) {
    const progressValue = Math.min(1, Math.max(0, t));
    const exact = progressValue / segment;
    const left = Math.min(stages.length - 1, Math.floor(exact));
    const right = Math.min(stages.length - 1, left + 1);
    const local = exact - left;

    stages.forEach((stage, index) => {
      let opacity = 0;
      if (index === left) opacity = 1 - local;
      if (index === right) opacity = Math.max(opacity, local);
      if (left === right && index === left) opacity = 1;
      stage.style.opacity = opacity;
      stage.style.transform = `scale(${1.035 - opacity * 0.015})`;
    });

    const nearest = Math.min(stages.length - 1, Math.round(exact));
    setMeta(nearest);
    progress.style.transform = `scaleX(${progressValue})`;
  }

  function animate(now) {
    if (startTime === null) startTime = now;
    const t = Math.min(1, (now - startTime) / duration);
    draw(t);

    if (t < 1) {
      requestAnimationFrame(animate);
      return;
    }

    finished = true;
    opening.classList.add('opening-complete');
    enter.removeAttribute('aria-hidden');
  }

  function begin() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      draw(1);
      finished = true;
      opening.classList.add('opening-complete');
      enter.removeAttribute('aria-hidden');
      return;
    }
    requestAnimationFrame(animate);
  }

  const firstImage = stages[0]?.querySelector('img');
  if (!firstImage || firstImage.complete) {
    begin();
  } else {
    const fallback = window.setTimeout(begin, 1800);
    const startOnce = () => {
      window.clearTimeout(fallback);
      begin();
    };
    firstImage.addEventListener('load', startOnce, { once: true });
    firstImage.addEventListener('error', startOnce, { once: true });
  }

  opening.addEventListener('click', (event) => {
    if (event.target.closest('a')) return;
    if (!finished) {
      startTime = performance.now() - duration;
    }
  });
}
