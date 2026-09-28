"""Edition-neutral Atlas reader assembly; no canonical edition content is embedded."""
import html
import re
import shutil
from pathlib import Path
from production_state import ROOT, read, write, binding, require_current, public_path, digest

GRAMMAR_VERSION='atlas-reader-v1'
def esc(value): return html.escape(str(value),quote=True)
def chunks(text, limit=38):
    """Paginate verbatim at sentence boundaries. Never summarize or drop evidence."""
    result=[]; current=[]
    for sentence in re.split(r'(?<=[.!?])\s+', text.strip()):
        if current and len((' '.join(current+[sentence])).split())>limit:
            result.append(' '.join(current));current=[]
        current.append(sentence)
    if current:result.append(' '.join(current))
    return result

def prose(block):
    return f'<h2>{esc(block["heading"])}</h2>'+''.join(f'<p><span class="state">{esc(p["state"])}</span>{esc(p["text"])}</p>'+refs(p) for p in block['paragraphs'])
def refs(p):
    return '<div class="refs">'+''.join(f'<a href="#source-{esc(r)}">{esc(r)}</a>' for r in p['evidence_refs'])+'</div>'
def label(asset):
    return ('Explanatory graphic' if asset['provider']=='ATLAS_DETERMINISTIC_GRAPHIC' else 'AI-generated contextual illustration · not a documentary photograph')+'. '+asset['truth_boundary']

def build_reader(run,edition,candidate,routes,story,assets,copy):
    sources=read(run/'source-register.json');by_scene={a['scene_id']:a for a in assets}
    hero_asset=next((a for a in assets if a['provider']!='ATLAS_DETERMINISTIC_GRAPHIC'),None)
    if not hero_asset:raise ValueError('publication reader requires contextual imagery')
    def scenes(block, sid, asset=None):
        parts=[(p,t) for p in block['paragraphs'] for t in chunks(p['text'])]
        result=[]
        for i,(p,text) in enumerate(parts):
            graphic=asset and asset['provider']=='ATLAS_DETERMINISTIC_GRAPHIC'
            cls='graphic' if graphic else 'scene-overlay' if asset else 'text-scene'
            picture=f'<img src="{esc(asset["path"])}" alt="{esc(block["heading"])}" loading="lazy">' if asset else ''
            if graphic:picture='<figure>'+picture+'</figure>'
            note=f'<span class="caption">{esc(label(asset))}</span>' if asset else ''
            result.append(f'<section class="scene {cls}" id="{esc(sid)}{("-part-"+str(i+1)) if i else ""}" data-scene="{esc(sid)}"><!-- Verbatim paragraph pagination -->{picture}<div class="scene-copy"><small>{esc(p["state"])} · {i+1:02d} / {len(parts):02d}</small><h2>{esc(block["heading"])}</h2><p data-prose>{esc(text)}</p>{refs(p)}{note}</div></section>')
        return ''.join(result)
    panels=[];entries=[]
    for ix,route in enumerate(routes):
        route_assets=[by_scene[s['scene_id']] for s in route['scenes'] if s['scene_id'] in by_scene]
        route_image=next((a for a in route_assets if a['provider']!='ATLAS_DETERMINISTIC_GRAPHIC'),None)
        menu_asset=route_image or next(iter(route_assets),None)
        if not menu_asset:menu_asset=hero_asset
        body=''.join(scenes(copy['scenes'][s['scene_id']],s['scene_id'],by_scene.get(s['scene_id']) or route_image) for s in route['scenes'])
        boundaries=''.join(f'<li>{esc(s["causal_boundary"])}</li>' for s in route['scenes'] if s.get('causal_boundary'))
        end=f'<footer class="boundary route-end"><small>{esc(route["perspective"])} · PERSPECTIVE COMPLETE</small><h2>This route ends here.</h2><p>Follow another part of this connected world.</p><details><summary>What this evidence can—and cannot—say</summary><ul>{boundaries}</ul></details><a class="route-exit" href="#perspectives">Choose what to explore next ↑</a><a class="route-exit" href="#story">STORY / FICTION</a></footer>'
        panels.append(f'<section data-view class="route" id="route-{esc(route["perspective_id"])}" hidden><nav class="route-nav"><a href="#perspectives">← Perspectives</a><span>{esc(route["perspective"])}</span></nav>{body}{end}</section>')
        entries.append(f'<a class="perspective {"diagram-choice" if menu_asset["provider"]=="ATLAS_DETERMINISTIC_GRAPHIC" else ""}" href="#route-{esc(route["perspective_id"])}" data-perspective="{esc(route["perspective_id"])}" style="--accent:hsl({(ix*67+30)%360} 65% 65%)"><img src="{esc(menu_asset["path"])}" alt="" loading="lazy"><div class="perspective-copy"><small>{ix+1:02d} / {len(routes):02d}</small><h2>{esc(route["perspective"])}</h2><p>{esc(route["scenes"][0]["meaning"])}</p></div><span class="arrow" aria-hidden="true">→</span></a>')
    source_html=''.join(f'<details id="source-{esc(s["id"])}"><summary>{esc(s["id"])} · {esc(s["title"])}</summary><p>Supports: {esc(s["supports"])}</p><p>Limit: {esc(s["limitation"])}</p><a href="{esc(s["url"])}" rel="noopener">Open source ↗</a></details>' for s in sources)
    media=read(run/'opening-media.json') if (run/'opening-media.json').exists() else {}
    if media.get('status')=='PASS':
        require_current(run,media)
        if media.get('visual_qa',{}).get('status')!='PASS' or digest(public_path(media['path']))!=media.get('sha256'):
            raise ValueError('approved opening film has invalid review or binary hash')
    film=media.get('path') if media.get('edition_id')==edition and media.get('status')=='PASS' and media.get('visual_qa',{}).get('status')=='PASS' else None
    sequence=[a for a in assets if a['provider']!='ATLAS_DETERMINISTIC_GRAPHIC'][:3]
    if not film and len(sequence)<2:raise ValueError('cinematic opening needs two independently verified contextual images or an approved film')
    mode='approved_film' if film else 'verified_image_sequence'
    write(run/'opening-system.json',{**binding(run),'status':'PASS','mode':mode,'assets':[{'path':a['path'],'sha256':a['sha256']} for a in sequence] if not film else [],'film':{'path':film,'sha256':media['sha256']} if film else None})
    film_html=(f'<video class="hero-video" autoplay muted playsinline preload="auto" poster="{esc(hero_asset["path"])}"><source src="{esc(film)}" type="video/mp4"></video><div class="film-mark"><span>ATLASOQUENCE</span><span>AI-GENERATED CONTEXTUAL FILM</span></div><button class="skip-film">Skip opening ↓</button><button class="play-film" hidden>Play opening film</button>') if film else ('<div class="opening-sequence" aria-hidden="true">'+''.join(f'<img src="{esc(a["path"])}" alt="" class="opening-frame frame-{i+1}">' for i,a in enumerate(sequence))+'</div><div class="film-mark"><span>ATLASOQUENCE</span><span>A CHANGING WORLD</span></div><button class="skip-film">Skip opening ↓</button>')
    menu_links='<nav class="menu-links"><a href="#edition">Edition</a><a href="#reality">What’s real</a><a href="#story">STORY / FICTION</a><a href="#consequences">Consequences</a><a href="#place">Place</a><a href="#sources">Sources</a></nav>'
    # Subtitle is existing editorial copy, not newly generated factual text.
    subtitle=routes[0]['scenes'][0]['meaning']
    if len(subtitle.split())>32:subtitle=candidate['geographic_core']
    story_html=''.join(f'<p>{esc(p)}</p>' for p in story['story'])
    shared=''.join(f'<section data-view class="route" id="{key}" hidden><nav class="route-nav"><a href="#perspectives">← Perspectives</a><span>{title}</span></nav>{scenes(copy[block],key+"-scene",hero_asset if key=="place" else None)}<footer class="boundary route-end"><h2>Where next?</h2><a href="#perspectives" class="route-exit">Choose a Perspective ↑</a></footer></section>' for key,block,title in [('reality','opening','WHAT’S REAL'),('place','place','PLACE'),('consequences','consequences','CONSEQUENCES')])
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#050708"><meta name="robots" content="noindex,nofollow"><title>{esc(candidate['working_title'])} · Atlasoquence</title><link rel="stylesheet" href="reader.css"><script src="reader.js" defer></script></head><body data-reader-grammar="{GRAMMAR_VERSION}"><main>
<section data-view id="edition"><header class="hero video-entry" data-opening-mode="{mode}"><img class="edition-geo-bg" src="{esc(hero_asset['path'])}" alt="{esc(candidate['geographic_core'])} · contextual illustration">{film_html}<div class="shade"></div><div class="edition-mark reveal-copy"><span>ATLASOQUENCE</span><span>{esc(edition)}</span></div><div class="media-notice" hidden></div><div class="hero-copy reveal-copy"><small>{esc(candidate['geographic_core'])} · A CHANGING WORLD</small><h1 tabindex="-1">{esc(candidate['working_title'])}</h1><p>{esc(subtitle)}</p><a class="enter" href="#perspectives">Choose a perspective ↓</a></div><span class="hero-caption">AI-generated contextual illustration · not documentary evidence</span></header></section>
<section data-view class="menu" id="perspectives" hidden><div class="menu-head"><small>PERSPECTIVES</small><h1>{len(routes)} perspectives. One connected world.</h1><p>Scroll, then choose where you want to enter.</p><span class="caption">Contextual illustrations and explanatory graphics · not documentary photographs</span></div><div class="perspective-list">{''.join(entries)}</div>{menu_links}</section>
{''.join(panels)}{shared}
<section data-view class="story" id="story" hidden><nav class="route-nav"><a href="#perspectives">← Perspectives</a><span>STORY / FICTION</span></nav><header class="boundary story-opening"><small>STORY / FICTION</small><h2>{esc(story['title'])}</h2><p class="boundary-label boundary">{esc(story['boundary'])}</p></header><div class="story-copy">{story_html}<aside><small>FICTION BOUNDARY</small><p>These people, dialogue and events are invented. This is not testimony.</p></aside><a class="route-exit" href="#perspectives">Choose what to explore next ↑</a></div></section>
<section data-view class="sources" id="sources" hidden><a href="#perspectives">← Perspectives</a><h1>Inspect the evidence.</h1>{source_html}<p>Facts can change the fiction. Fiction must never quietly become fact.</p></section></main></body></html>'''
    target=ROOT/'public/review'/edition.lower();target.mkdir(parents=True,exist_ok=True)
    (target/'index.html').write_text(page,encoding='utf8')
    for source,destination in [('reader-production.css','reader.css'),('reader-production.js','reader.js')]:shutil.copyfile(ROOT/'public/review'/source,target/destination)
    return target/'index.html'
