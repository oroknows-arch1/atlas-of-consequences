(() => {
  const $ = (sel, root = document) => root.querySelector(sel);
  const make = (tag, className, html) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (html !== undefined) el.innerHTML = html;
    return el;
  };

  const report = $('#report .content');
  if (report && !$('.fact-strip', report)) {
    const strip = make('div', 'fact-strip');
    const facts = [
      ['415 TWh', 'Global data-centre electricity use in 2024 · IEA'],
      ['~1.5%', 'Share of global electricity consumption in 2024 · IEA'],
      ['58%', 'Antofagasta share of projected Chilean copper production in 2025 · Cochilco'],
      ['~15 km', 'Chuquicamata north of Calama · Codelco'],
      ['266 kt', 'Chuquicamata fine-copper production in 2025 · Codelco'],
      ['3,992', 'Direct Chuquicamata employees at end-2025 · Codelco']
    ];
    facts.forEach(([value, label]) => {
      const card = make('div', 'fact-callout');
      const strong = document.createElement('strong');
      strong.textContent = value;
      const span = document.createElement('span');
      span.textContent = label;
      card.append(strong, span);
      strip.append(card);
    });
    const h2 = $('h2', report);
    h2.insertAdjacentElement('afterend', strip);
  }

  const consequences = $('#consequences .content');
  if (consequences && !$('.certainty-map', consequences)) {
    const map = make('div', 'certainty-map');
    const layers = [
      ['01 · DOCUMENTED GLOBAL', 'AI/data-centre expansion → electricity demand → generation/grid/infrastructure → material requirements including copper.'],
      ['02 · DOCUMENTED PLACE', 'Copper → Chile → Antofagasta Region → Calama / Chuquicamata copper economy.'],
      ['03 · FICTIONAL HUMAN', 'Mauricio’s opportunity and its household consequences are invented exploration, not evidence or forecast.']
    ];
    layers.forEach(([label, text]) => {
      const card = make('div', 'certainty-card');
      const lab = make('div', 'label');
      lab.textContent = label;
      const p = document.createElement('p');
      p.textContent = text;
      card.append(lab, p);
      map.append(card);
    });
    const introParas = consequences.querySelectorAll(':scope > p');
    const anchor = introParas.length > 1 ? introParas[1] : $('h2', consequences);
    anchor.insertAdjacentElement('afterend', map);

    [...consequences.querySelectorAll('p')].forEach(p => {
      if (p.textContent.trim() === 'AI boom → mine expands → Mauricio gets promoted.') {
        p.classList.add('prohibited-boundary');
        const lab = make('div', 'label');
        lab.textContent = 'PROHIBITED CAUSAL SHORTCUT';
        p.prepend(lab);
      }
    });
  }

  const place = $('#place .content');
  if (place && !$('.location-card', place)) {
    const card = make('div', 'location-card');
    const lab = make('div', 'label');
    lab.textContent = 'PLACE · REAL LOCATION';
    const route = make('div', 'route');
    route.textContent = 'Calama → El Loa → Antofagasta Region → Chile';
    const p = document.createElement('p');
    p.textContent = 'Chuquicamata lies about 15 km north of Calama. The household is fictional; the city, region and mining setting are real.';
    const a = document.createElement('a');
    a.href = 'https://www.openstreetmap.org/search?query=Calama%2C%20Chile';
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.textContent = 'View Calama on OpenStreetMap';
    card.append(lab, route, p, a);
    $('h2', place).insertAdjacentElement('afterend', card);
  }

  const sourcesRoot = $('#sources .content');
  const sourceData = [
    {
      id:'SR-01', title:'Global data-centre electricity use', publisher:'International Energy Agency · Energy and AI — Executive summary · 10 Apr 2025',
      role:'Supports about 415 TWh of data-centre electricity use in 2024 and about 1.5% of global electricity consumption.',
      limitation:'Data-centre total; not AI alone and not a universal per-query footprint.',
      links:[['Primary source','https://www.iea.org/reports/energy-and-ai/executive-summary']]
    },
    {
      id:'SR-02', title:'AI and projected data-centre electricity growth', publisher:'International Energy Agency · Energy and AI · 2025',
      role:'Supports the data-centre electricity growth outlook and AI as an important driver.',
      limitation:'Forecasts are scenario/model outputs, not guarantees.',
      links:[['Energy demand from AI','https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai'],['Energy supply for AI','https://www.iea.org/reports/energy-and-ai/energy-supply-for-ai']]
    },
    {
      id:'SR-03', title:'Data centres are physical infrastructure', publisher:'International Energy Agency · Energy and AI · 2025',
      role:'Supports servers, storage, networking, cooling, grid connection and backup systems as physical facility components.',
      limitation:'Facility configurations differ materially.',
      links:[['Primary source','https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai']]
    },
    {
      id:'SR-04', title:'Grid constraints and copper/material requirements', publisher:'International Energy Agency · AI and energy security · 2025',
      role:'Supports power-equipment supply pressure and materials including copper associated with data-centre and electricity infrastructure.',
      limitation:'Does not establish AI as the sole or dominant source of total copper demand.',
      links:[['Primary source','https://www.iea.org/reports/energy-and-ai/ai-and-energy-security']]
    },
    {
      id:'SR-05', title:'Antofagasta share of Chilean copper production', publisher:'Cochilco · 2025–2034 copper production projection · 2025',
      role:'Supports Antofagasta at 58% of projected national production in 2025 and remaining the principal regional production centre.',
      limitation:'Projection, not observed future production; mining activity has many drivers independent of AI.',
      links:[['Primary source','https://www.cochilco.cl/web/download/975/2025/15321/proyeccion-de-la-produccion-de-cobre-en-chile-periodo-2025-2034.pdf']]
    },
    {
      id:'SR-06', title:'Chilean copper production context', publisher:'Cochilco · monthly electronic bulletin · 2026 updates',
      role:'Supports official Chilean copper-production statistics and the established scale of the copper system.',
      limitation:'Production statistics do not attribute demand to particular end uses.',
      links:[['Primary source','https://boletin.cochilco.cl/']]
    },
    {
      id:'SR-07', title:'Chuquicamata operation, production and workforce', publisher:'Codelco · Chuquicamata operations · current operational data 2025',
      role:'Supports operation context, 266 thousand tonnes of fine copper in 2025 and 3,992 direct employees at 31 Dec 2025.',
      limitation:'Company primary source; strongest for its own operational data, not independent social evaluation.',
      links:[['Primary source','https://www.codelco.com/chuquicamata']]
    },
    {
      id:'SR-08', title:'Chuquicamata approximately 15 km north of Calama', publisher:'Codelco · Memoria Integrada 2025 · published 2026',
      role:'Supports the stated distance and direction between Chuquicamata and Calama.',
      limitation:'Company primary source.',
      links:[['Primary source','https://www.codelco.com/prontus_codelco/site/docs/20260330/20260330133750/codelco_memoria2025.pdf']]
    },
    {
      id:'SR-09', title:'Calama population', publisher:'INE Chile · Censo 2024, Antofagasta results · 2025 release',
      role:'Supports the 2024 census count of 166,334 people in Calama.',
      limitation:'Census population measure; not an estimate of current 2026 population.',
      links:[['Primary source','https://censo2024.ine.gob.cl/wp-content/uploads/2025/03/02_PRESENTACION-R_REGIONAL-ANTOFAGASTA.pdf']]
    },
    {
      id:'SR-10', title:'Mining labour commuting and home-life context', publisher:'Universidad Católica del Norte · 22 Jul 2025',
      role:'Supports labour commuting as a documented feature of mining around Antofagasta and Calama.',
      limitation:'Qualitative research; does not make the fictional household representative of all mining families.',
      links:[['Primary source','https://www.ucn.cl/comunicaciones-ucn/noticias/estudio-identifica-factores-que-incentivan-la-conmutacion-en-la-mineria/']]
    },
    {
      id:'SR-11', title:'7x7 roster documented in Chuquicamata', publisher:'Codelco · 2013 and 2020 operational records',
      role:'Supports 7x7 roster plausibility in the Chuquicamata work environment.',
      limitation:'Does not establish Mauricio’s exact fictional roster, hours or rotation sequence.',
      links:[['2013 record','https://www.codelco.com/operaciones/chuquicamata/noticias/formalizan-historico-cambio-de-jornada-laboral-en-chuquicamata'],['2020 record','https://www.codelco.com/prensa/2020/medida-covid-19-division-chuquicamata-inicia-jornada-7x7-en-todas-sus']]
    },
    {
      id:'SR-12', title:'Organised worker transport', publisher:'Codelco · transport records · 2020/2022',
      role:'Supports organised personnel transport between Calama and Chuquicamata-related destinations.',
      limitation:'Does not establish Mauricio’s fictional pickup point, operator, route or journey time.',
      links:[['Transport tender','https://www.codelco.com/prontus_codelco/site/docs/20201006/20201006103545/rsm_ejecutivo_proceso_n___8000001799_rev2.pdf'],['Electric buses','https://www.codelco.com/prensa/2022/mineros-y-mineras-de-codelco-se-transportaran-en-los-primeros-buses']]
    },
    {
      id:'SR-13', title:'Contemporary Calama resident context', publisher:'Universidad Católica del Norte · Barómetro Regional Calama · current series includes 2026',
      role:'Supports contemporary resident concerns and the wider lived-city context beyond mining alone.',
      limitation:'Survey findings do not describe the fictional household; serious local conditions are not imported into STORY without a separate evidence decision.',
      links:[['Primary source','https://politicaspublicasdelnorte.cl/encuestas/calama']]
    },
    {
      id:'SR-14', title:'Chuquicamata relocation to Calama', publisher:'Codelco · 2007 sustainability report and historical record',
      role:'Supports the relocation of more than 10,000 people and the 2007 closure chronology of the former camp.',
      limitation:'Codelco was a participant in the relocation; use for chronology and scale, not independent evaluation of social outcomes.',
      links:[['2007 report','https://www.codelco.com/prontus_codelco/site/docs/20160311/20160311171654/reportecodelco2007.pdf'],['Historical record','https://www.codelco.com/sustentabilidad/publicaciones/informe-sustentable/chuquicamata-92-anos-de-historia']]
    },
    {
      id:'SR-15', title:'Chuquicamata heritage and local identity', publisher:'Servicio Nacional del Patrimonio Cultural · 2015 + official heritage record',
      role:'Supports recognised historical, social, territorial, urban and architectural significance of the former camp.',
      limitation:'Heritage evidence establishes significance and status; it does not by itself describe every resident’s lived experience.',
      links:[['Heritage declaration record','https://www.patrimoniocultural.gob.cl/noticias/cmn-se-pronuncio-favor-de-declaratoria-de-chuquicamata-como-zona-tipica-y-monumento'],['Official heritage record','https://ide.patrimoniocultural.gob.cl/patrimonio/705']]
    },
    {
      id:'SR-16', title:'Indigenous context and sourcing boundary', publisher:'Ministerio de Energía, Chile · participation records · 2024',
      role:'Supports documented Lickanantay participation in the wider Antofagasta regional context.',
      limitation:'Does not establish a specific Calama community viewpoint or permit Atlas to speak for an Indigenous community.',
      links:[['Primary source','https://energia.gob.cl/sites/default/files/documentos/20241206_informe_consulta_ciudadana_plan_energia_pagenumber.pdf']]
    }
  ];

  if (sourcesRoot && !$('.source-register', sourcesRoot)) {
    const register = make('div', 'source-register');
    const heading = document.createElement('h3');
    heading.textContent = 'Inspect the evidence';
    const intro = make('p', 'source-register-intro');
    intro.textContent = 'Each card shows what the source supports and where its limit sits. Evidence for the physical chain does not turn the fictional family into factual testimony.';
    register.append(heading, intro);

    sourceData.forEach(source => {
      const details = make('details', 'source-card');
      const summary = document.createElement('summary');
      summary.textContent = `${source.id} — ${source.title}`;
      const body = make('div', 'source-body');
      const meta = make('div', 'meta');
      meta.textContent = source.publisher;
      const role = document.createElement('p');
      role.innerHTML = `<strong>Supports:</strong> ${source.role}`;
      const limitation = make('p', 'limit');
      limitation.innerHTML = `<strong>Limitation:</strong> ${source.limitation}`;
      const links = document.createElement('p');
      source.links.forEach(([label, url], index) => {
        const a = document.createElement('a');
        a.href = url;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.textContent = label;
        if (index) links.append(document.createTextNode(' · '));
        links.append(a);
      });
      body.append(meta, role, limitation, links);
      details.append(summary, body);
      register.append(details);
    });

    sourcesRoot.append(register);
  }

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {
    const video = $('#factFilm');
    if (video) {
      video.pause();
      video.removeAttribute('autoplay');
      video.setAttribute('poster', 'assets/aoc001-report-video-candidate-v0.4-review.jpg');
    }
    const soundBtn = $('#soundBtn');
    if (soundBtn) soundBtn.style.display = 'none';
    if (typeof enterReader === 'function') enterReader();
  }
})();

/* Reader architecture v0.2: edition map, explicit mechanism flow and perspective story model. */
(() => {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const make = (tag, className, text) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  };

  const intro = $('#intro');
  if (intro && !$('.edition-map', intro)) {
    intro.classList.add('edition-map-screen');
    const inner = $('.intro-inner', intro);
    const map = make('div', 'edition-map');
    map.setAttribute('aria-label', 'What this edition will show');
    const kicker = make('div', 'edition-map-kicker', 'WHAT THIS SCROLL WILL SHOW');
    kicker.style.gridColumn = '1 / -1';
    map.append(kicker);

    const items = [
      ['01', "WHAT'S REAL", 'The documented change and the physical chain behind it', '#report'],
      ['02', 'STORY', 'A fictional human lens living inside that real system', '#story'],
      ['03', 'CONSEQUENCES', 'What is documented, what is connected, and what is only explored', '#consequences'],
      ['04', 'PLACE', 'Why the chain narrows to Calama and northern Chile', '#place'],
      ['05', 'SOURCES', 'Inspect the evidence and the limits of each claim', '#sources']
    ];

    items.forEach(([no, label, description, href]) => {
      const a = document.createElement('a');
      a.className = 'edition-map-item';
      a.href = href;
      const n = make('span', 'edition-map-no', no);
      const copy = make('span', 'edition-map-copy');
      const strong = document.createElement('strong');
      strong.textContent = label;
      const small = document.createElement('span');
      small.textContent = description;
      copy.append(strong, small);
      a.append(n, copy);
      map.append(a);
    });

    const prompt = make('div', 'edition-map-prompt', 'Scroll to follow the chain · tap a section to jump');
    prompt.style.gridColumn = '1 / -1';
    map.append(prompt);
    inner.append(map);
  }

  const nav = $('nav[aria-label="Edition sections"]');
  if (nav) {
    nav.classList.add('reader-route');
    const navLinks = $$('a', nav);
    navLinks.forEach(a => a.dataset.target = a.getAttribute('href') || '');
    const sections = ['report','story','consequences','place','sources']
      .map(id => document.getElementById(id))
      .filter(Boolean);
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        const visible = entries
          .filter(entry => entry.isIntersecting)
          .sort((a,b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (!visible) return;
        navLinks.forEach(a => a.classList.toggle('active', a.dataset.target === `#${visible.target.id}`));
      }, { rootMargin: '-24% 0px -58% 0px', threshold: [0,.05,.2,.45] });
      sections.forEach(section => observer.observe(section));
    }
  }

  const orientations = {
    report: "WHAT'S REAL · documented mechanism and evidence chain",
    story: 'STORY · fictional human perspective inside the system',
    consequences: 'CONSEQUENCES · separate documented effects from explored possibilities',
    place: 'PLACE · locate the mechanism in a real city and region',
    sources: 'SOURCES · inspect what each claim can and cannot prove'
  };
  Object.entries(orientations).forEach(([id, label]) => {
    const root = $(`#${id} .content`);
    if (!root || $('.chapter-orientation', root)) return;
    const idx = $('.idx', root);
    if (!idx) return;
    const orient = make('div', 'chapter-orientation');
    orient.append(make('span', '', 'WHERE YOU ARE'), make('strong', '', label));
    idx.insertAdjacentElement('afterend', orient);
  });

  const report = $('#report .content');
  if (report && !$('.signal-flow', report)) {
    const flow = make('div', 'signal-flow');
    flow.append(make('div', 'signal-flow-head', 'THE CONNECTION THIS EDITION IS TESTING'));
    const nodes = [
      ['01', 'AI / data-centre growth', 'More digital capacity means more physical computing infrastructure.', 'IEA · SR-01–03'],
      ['02', 'Electricity + grid demand', 'Facilities need generation, connections, transformers, substations, cables and other equipment.', 'IEA · SR-02–04'],
      ['03', 'Material demand', 'Copper is one of the materials used across data centres and the wider electricity system.', 'IEA · SR-04'],
      ['04', 'Northern Chile', 'Antofagasta is already the dominant copper-producing region in Chile.', 'Cochilco · SR-05–06'],
      ['05', 'Calama / Chuquicamata', 'The global material chain meets a real city, workforce, businesses and families.', 'Codelco + UCN · SR-07–12']
    ];
    nodes.forEach(([step, title, copy, source]) => {
      const node = make('div', 'flow-node');
      const num = make('span', 'flow-step', step);
      const text = make('div', 'flow-copy');
      const strong = document.createElement('strong');
      strong.textContent = title;
      const span = document.createElement('span');
      span.textContent = copy;
      const evidence = make('span', 'flow-evidence', source);
      text.append(strong, span, evidence);
      node.append(num, text);
      flow.append(node);
    });
    const boundary = make('div', 'flow-boundary');
    boundary.innerHTML = '<strong>Boundary:</strong> this is a documented connection chain, not proof that AI caused a specific Antofagasta mine expansion or a particular job.';
    flow.append(boundary);

    const factStrip = $('.fact-strip', report);
    const h2 = $('h2', report);
    if (factStrip) factStrip.insertAdjacentElement('beforebegin', flow);
    else h2.insertAdjacentElement('afterend', flow);
  }

  const story = $('#story .content');
  if (story && !$('.story-lens', story)) {
    const panel = make('div', 'story-lens');
    panel.append(make('div', 'label', 'CURRENT STORY LENS'));
    const title = document.createElement('h3');
    title.textContent = 'Inside → out · family + labour';
    const p = document.createElement('p');
    p.textContent = 'One market can look different depending on where you stand. AOC-001 currently follows the family and labour side of the copper system. The Atlas framework can support additional story branches without turning fiction into market evidence.';
    const grid = make('div', 'story-lens-grid');
    const lenses = [
      ['CURRENT', 'Family + labour', true],
      ['FRAMEWORK', 'Operator + supplier', false],
      ['FRAMEWORK', 'Buyer + customer', false],
      ['FRAMEWORK', 'Investor + market', false]
    ];
    lenses.forEach(([state, label, current]) => {
      const chip = make('div', `story-lens-chip${current ? ' current' : ''}`);
      chip.append(make('strong', '', state), document.createTextNode(label));
      grid.append(chip);
    });
    panel.append(title, p, grid);
    const boundary = $('.boundary-tag', story);
    if (boundary) boundary.insertAdjacentElement('beforebegin', panel);
    else $('h2', story).insertAdjacentElement('afterend', panel);
  }
})();
