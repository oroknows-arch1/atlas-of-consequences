const CONTENT_ROOT = "../content/AOC-001";
const MASTER_EDITION = `${CONTENT_ROOT}/master-edition-v0.1.md`;
const SOURCE_REGISTER = `${CONTENT_ROOT}/sources/publication-source-register-v0.1.md`;

const SECTION_CONFIG = [
  { id: "whats-real", match: (title) => title === "WHAT'S REAL", title: "WHAT'S REAL", mode: "SOURCED FACTS" },
  { id: "story", match: (title) => title.startsWith("STORY"), title: "STORY", mode: "FICTION" },
  { id: "consequences", match: (title) => title === "CONSEQUENCES", title: "CONSEQUENCES", mode: "CONNECTIONS" },
  { id: "place", match: (title) => title === "PLACE", title: "PLACE", mode: "LOCAL CONTEXT" },
  { id: "sources", match: (title) => title === "SOURCES", title: "SOURCES", mode: "EVIDENCE REGISTER" }
];

const edition = document.querySelector("#edition");
const progressBar = document.querySelector("#progressBar");

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function inlineMarkdown(value) {
  let text = escapeHtml(value);

  text = text.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  text = text.replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
  text = text.replace(/`([^`]+)`/g, "<code>$1</code>");
  text = text.replace(
    /(https?:\/\/[^\s<]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
  );

  return text;
}

function markdownToHtml(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const output = [];
  let paragraph = [];
  let listType = null;
  let listItems = [];
  let quote = [];

  function flushParagraph() {
    if (!paragraph.length) return;
    output.push(`<p>${inlineMarkdown(paragraph.join("\n")).replaceAll("\n", "<br>")}</p>`);
    paragraph = [];
  }

  function flushList() {
    if (!listType || !listItems.length) return;
    output.push(`<${listType}>${listItems.map((item) => `<li>${inlineMarkdown(item)}</li>`).join("")}</${listType}>`);
    listType = null;
    listItems = [];
  }

  function flushQuote() {
    if (!quote.length) return;
    output.push(`<blockquote>${inlineMarkdown(quote.join("\n")).replaceAll("\n", "<br>")}</blockquote>`);
    quote = [];
  }

  function flushAll() {
    flushParagraph();
    flushList();
    flushQuote();
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();

    if (!line.trim()) {
      flushAll();
      continue;
    }

    const h3 = line.match(/^###\s+(.+)$/);
    const h2 = line.match(/^##\s+(.+)$/);
    const h1 = line.match(/^#\s+(.+)$/);

    if (h3 || h2 || h1) {
      flushAll();
      const heading = h3?.[1] || h2?.[1] || h1?.[1];
      const tag = h3 ? "h3" : "h2";
      output.push(`<${tag}>${inlineMarkdown(heading)}</${tag}>`);
      continue;
    }

    if (/^---+$/.test(line.trim())) {
      flushAll();
      output.push("<hr>");
      continue;
    }

    const bullet = line.match(/^[-*]\s+(.+)$/);
    const numbered = line.match(/^\d+\.\s+(.+)$/);

    if (bullet || numbered) {
      flushParagraph();
      flushQuote();
      const desiredType = bullet ? "ul" : "ol";
      if (listType && listType !== desiredType) flushList();
      listType = desiredType;
      listItems.push(bullet?.[1] || numbered?.[1]);
      continue;
    }

    const blockquote = line.match(/^>\s?(.*)$/);
    if (blockquote) {
      flushParagraph();
      flushList();
      quote.push(blockquote[1]);
      continue;
    }

    flushList();
    flushQuote();
    paragraph.push(line);
  }

  flushAll();
  return output.join("\n");
}

function extractTopLevelSections(markdown) {
  const matches = [...markdown.matchAll(/^#\s+(.+)$/gm)];
  const sections = [];

  matches.forEach((match, index) => {
    const title = match[1].trim();
    const bodyStart = match.index + match[0].length;
    const bodyEnd = matches[index + 1]?.index ?? markdown.length;
    sections.push({ title, body: markdown.slice(bodyStart, bodyEnd).trim() });
  });

  return sections;
}

function stripLeadingHeading(markdown) {
  return markdown.replace(/^#\s+.+\n+/, "").trim();
}

function storyBoundary(body) {
  const paragraphs = body.split(/\n\s*\n/);
  const first = paragraphs[0]?.trim() || "";

  if (!first.startsWith("**Fiction boundary:**")) {
    return { boundary: "", body };
  }

  return {
    boundary: first,
    body: paragraphs.slice(1).join("\n\n").trim()
  };
}

function renderSection(config, body, index) {
  const section = document.createElement("section");
  section.className = `edition-section ${config.id}`;
  section.id = config.id;
  section.dataset.section = config.id;

  let boundaryHtml = "";
  let renderBody = body;

  if (config.id === "story") {
    const story = storyBoundary(body);
    renderBody = story.body;
    if (story.boundary) {
      boundaryHtml = `<div class="story-boundary">${markdownToHtml(story.boundary)}</div>`;
    }
  }

  section.innerHTML = `
    <div class="section-kicker">
      <span class="section-index">0${index + 1}</span>
      <span class="mode-label">${config.mode}</span>
    </div>
    <h2 class="section-title">${config.title}</h2>
    ${boundaryHtml}
    <div class="markdown-body">${markdownToHtml(renderBody)}</div>
    ${config.id === "sources" ? '<p class="source-note">Source links open the original evidence in a new tab. The register states what each source supports and where its limits are.</p>' : ""}
  `;

  return section;
}

async function loadEdition() {
  try {
    const [masterResponse, sourceResponse] = await Promise.all([
      fetch(MASTER_EDITION),
      fetch(SOURCE_REGISTER)
    ]);

    if (!masterResponse.ok) throw new Error(`Master edition failed to load (${masterResponse.status})`);
    if (!sourceResponse.ok) throw new Error(`Source register failed to load (${sourceResponse.status})`);

    const [masterMarkdown, sourceMarkdown] = await Promise.all([
      masterResponse.text(),
      sourceResponse.text()
    ]);

    const sourceSections = extractTopLevelSections(masterMarkdown);
    edition.innerHTML = "";

    SECTION_CONFIG.forEach((config, index) => {
      let body;

      if (config.id === "sources") {
        body = stripLeadingHeading(sourceMarkdown);
      } else {
        const matchedSection = sourceSections.find((section) => config.match(section.title));
        if (!matchedSection) throw new Error(`Missing locked section: ${config.title}`);
        body = matchedSection.body;
      }

      edition.appendChild(renderSection(config, body, index));
    });

    initialiseReaderNavigation();

    if (window.location.hash) {
      requestAnimationFrame(() => {
        document.querySelector(window.location.hash)?.scrollIntoView();
      });
    }
  } catch (error) {
    edition.innerHTML = `
      <section class="error-state">
        <div>
          <strong>AOC-001 could not be loaded.</strong>
          <p>${escapeHtml(error.message)}</p>
        </div>
      </section>
    `;
  }
}

function initialiseReaderNavigation() {
  const sections = [...document.querySelectorAll("[data-section]")];
  const navLinks = [...document.querySelectorAll("[data-nav]")];
  const nav = document.querySelector(".section-nav");
  let ticking = false;

  function updateReaderState() {
    const marker = window.scrollY + nav.offsetHeight + 44;
    let active = sections[0]?.id;

    for (const section of sections) {
      if (section.offsetTop <= marker) active = section.id;
    }

    navLinks.forEach((link) => {
      const isActive = link.dataset.nav === active;
      if (isActive) {
        link.setAttribute("aria-current", "page");
        link.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
      } else {
        link.removeAttribute("aria-current");
      }
    });

    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollable > 0 ? Math.min(1, window.scrollY / scrollable) : 0;
    progressBar.style.width = `${progress * 100}%`;

    ticking = false;
  }

  function requestUpdate() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(updateReaderState);
  }

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate);
  updateReaderState();
}

loadEdition();
