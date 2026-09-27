"""Edition-neutral reader assembly. Content and required images are upstream contracts."""
import html
import shutil
from pathlib import Path
from production_state import ROOT, read

def esc(value):
    return html.escape(str(value), quote=True)

def prose(block):
    paragraphs = []
    for p in block['paragraphs']:
        refs = ' '.join(f'<a href="#source-{esc(r)}">{esc(r)}</a>' for r in p['evidence_refs'])
        paragraphs.append(f'<p><small>{esc(p["state"])}</small><br>{esc(p["text"])}</p><p class="refs">{refs}</p>')
    return f'<h2>{esc(block["heading"])}</h2>' + ''.join(paragraphs)

def build_reader(run, edition, candidate, routes, story, assets, copy):
    sources = read(run/'source-register.json')
    override_path = run/'source-access-overrides.json'
    if override_path.exists():
        overrides = read(override_path)
        for source in sources:
            source.update(overrides.get(source['id'], {}))
    by_scene = {a['scene_id']: a for a in assets}
    def media(asset, meaning):
        label = 'Explanatory graphic' if asset['provider'] == 'ATLAS_DETERMINISTIC_GRAPHIC' else 'AI-generated contextual illustration · not a documentary photograph'
        return f'<figure><img src="{esc(asset["path"])}" alt="{esc(meaning)}" loading="lazy"><figcaption>{label}. {esc(asset["truth_boundary"])}</figcaption></figure>'
    panels = []
    for route in routes:
        scenes = []
        for scene in route['scenes']:
            visual = media(by_scene[scene['scene_id']], scene['meaning']) if scene['scene_id'] in by_scene else ''
            scenes.append(f'<section class="scene" id="{esc(scene["scene_id"])}">{visual}<div class="scene-copy">{prose(copy["scenes"][scene["scene_id"]])}</div></section>')
        panels.append(f'<section data-view class="route" id="route-{esc(route["perspective_id"])}"><nav><a href="#perspectives">← Edition choices</a><span>{esc(route["perspective"])}</span></nav><h1 tabindex="-1">{esc(route["perspective"])}</h1>{"".join(scenes)}<footer><b>ROUTE COMPLETE</b><p>Where would you like to go next?</p><a href="#perspectives">Choose a Perspective</a> · <a href="#story">Read the STORY</a> · <a href="#consequences">Explore consequences</a></footer></section>')
    nav = ''.join(f'<a href="#route-{esc(r["perspective_id"])}">{esc(r["perspective"])}</a>' for r in routes)
    hero_asset = next((a for a in assets if a['provider'] != 'ATLAS_DETERMINISTIC_GRAPHIC'), None)
    if not hero_asset:
        raise ValueError('publication reader requires contextual imagery')
    def source_links(source):
        links = [f'<a href="{esc(source["url"])}" rel="noopener">Open source ↗</a>']
        for fallback in source.get("fallback_urls", []):
            links.append(f'<a href="{esc(fallback)}" rel="noopener">Canonical access ↗</a>')
        return " · ".join(links)
    sources_html = ''.join(f'<details id="source-{esc(s["id"])}"><summary>{esc(s["id"])} · {esc(s["title"])}</summary><p>Supports: {esc(s["supports"])}</p><p>Limit: {esc(s["limitation"])}</p>{source_links(s)}</details>' for s in sources)
    story_html = ''.join(f'<p>{esc(p)}</p>' for p in story['story'])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow"><title>{esc(candidate['working_title'])} · Atlasoquence</title><link rel="stylesheet" href="reader.css"><script src="reader.js" defer></script></head><body>
<header class="edition-header"><a href="#edition">ATLASOQUENCE · {esc(candidate['working_title'])}</a><nav aria-label="Edition"><a href="#perspectives">Perspectives</a><a href="#story">STORY</a><a href="#place">PLACE</a><a href="#sources">SOURCES</a></nav><small>UNPUBLISHED · AUTOMATED QA BUILD</small></header><main>
<section data-view id="edition"><header class="hero"><small>{esc(candidate['geographic_core'])} · WHAT’S REAL</small><h1 tabindex="-1">{esc(candidate['working_title'])}</h1>{media(hero_asset, candidate['world_change'])}</header><article class="opening">{prose(copy['opening'])}<a href="#perspectives">Choose your way in ↓</a></article></section>
<section data-view class="menu" id="perspectives"><small>ONE EDITION · READER-SELECTED ROUTES</small><h1 tabindex="-1">Choose your way in.</h1><div class="cards">{nav}</div><p><a href="#edition">Read the factual opening</a> · <a href="#story">STORY</a> · <a href="#consequences">CONSEQUENCES</a> · <a href="#place">PLACE</a></p></section>
{''.join(panels)}
<section data-view class="story" id="story"><div class="story-inner"><small>STORY / FICTION</small><h1 tabindex="-1">{esc(story['title'])}</h1><p class="boundary">{esc(story['boundary'])}</p>{story_html}<aside><b>FICTION BOUNDARY</b><p>These people, dialogue and events are invented. This is not testimony.</p></aside><a href="#perspectives">Choose what to explore next</a></div></section>
<section data-view class="sources" id="consequences"><small>CONSEQUENCES · FACT AND UNCERTAINTY</small>{prose(copy['consequences'])}<a href="#perspectives">Return to edition choices</a></section>
<section data-view class="sources" id="place"><small>PLACE · GEOGRAPHIC CONTEXT</small>{prose(copy['place'])}<a href="#perspectives">Return to edition choices</a></section>
<section data-view class="sources" id="sources"><h1 tabindex="-1">Inspect the evidence.</h1>{sources_html}<p>Facts can change the fiction. Fiction must never quietly become fact.</p><a href="#perspectives">Return to edition choices</a></section></main></body></html>'''
    target = ROOT/'public'/'review'/edition.lower()
    target.mkdir(parents=True, exist_ok=True)
    (target/'index.html').write_text(page, encoding='utf8')
    for source, destination in [('reader-production.css', 'reader.css'), ('reader-production.js', 'reader.js')]:
        shutil.copyfile(ROOT/'public'/'review'/source, target/destination)
    return target/'index.html'
