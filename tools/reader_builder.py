"""Populate the AOC-001 adaptive reader surface from accepted edition inputs.

The adaptive CSS and opening/navigation controller are copied from the canonical
reader. This module supplies editorial data; it never designs another reader.
"""
import hashlib
import html
import re
import shutil
from pathlib import Path
from production_state import ROOT, read, write, binding, digest, public_path

CANONICAL = ROOT / 'public/adaptive'
def esc(value): return html.escape(str(value), quote=True)
def chunks(value, limit=38):
    out=[]; current=[]
    for sentence in re.split(r'(?<=[.!?])\s+', value.strip()):
        if current and len(' '.join(current+[sentence]).split())>limit:
            out.append(' '.join(current)); current=[]
        current.append(sentence)
    if current: out.append(' '.join(current))
    return out

def build_reader(run, edition, candidate, routes, story, assets, copy, *, structural=False):
    """Structural previews reuse persisted assets without claiming asset coverage."""
    sources=read(run/'source-register.json')
    source_ids={s['id'] for s in sources}
    available=[a for a in assets if public_path(a['path']).is_file() and
               digest(public_path(a['path']))==a.get('sha256') and
               a.get('visual_qa',{}).get('pass') is True]
    if not available: raise ValueError('no verified persisted preview asset')
    by_scene={a['scene_id']:a for a in available if not a.get('beat_id')}
    by_beat={a['beat_id']:a for a in available if a.get('beat_id')}
    contextual=[a for a in available if a['provider']!='ATLAS_DETERMINISTIC_GRAPHIC']
    if len(contextual)<2: raise ValueError('opening requires two verified contextual assets')
    hero=contextual[0]
    media=read(run/'opening-media.json') if (run/'opening-media.json').exists() else {}
    film=(media.get('path') if media.get('edition_id')==edition and media.get('status')=='PASS'
          and media.get('visual_qa',{}).get('status')=='PASS' and
          media.get('path') and digest(public_path(media['path']))==media.get('sha256') else None)
    sequence=contextual[:3]
    opening=('''<video class="hero-video" autoplay muted playsinline preload="auto" poster="%s"><source src="%s" type="video/mp4"></video>'''%(esc(hero['path']),esc(film))) if film else '<div class="opening-sequence" aria-hidden="true">'+''.join('<img src="%s" alt="" class="opening-frame frame-%d">'%(esc(a['path']),i+1) for i,a in enumerate(sequence))+'</div>'
    mode='approved_film' if film else 'verified_image_sequence'
    write(run/'opening-system.json',{**binding(run),'status':'PASS','mode':mode,
          'assets':[{'path':a['path'],'sha256':a['sha256']} for a in sequence] if not film else [],
          'film':{'path':film,'sha256':media['sha256']} if film else None})

    def scene(block, sid, asset):
        bits=[]
        for p in block['paragraphs']:
            if p['state'] not in ('FACT','UNCERTAIN','STORY') or set(p['evidence_refs'])-source_ids:
                raise ValueError('unverified truth state or evidence reference')
            bits.extend((p,t) for t in chunks(p['text']))
        result=[]
        for n,(p,text) in enumerate(bits,1):
            beat=by_beat.get(f'{sid}-B{n}') or (asset if n==1 else None)
            # A structural preview may repeat a verified image; it never calls
            # that repetition finished visual coverage or publication evidence.
            if not beat and structural: beat=asset or hero
            graphic=beat and beat['provider']=='ATLAS_DETERMINISTIC_GRAPHIC'
            cls='graphic' if graphic else 'scene-overlay' if beat else 'text-scene'
            image='<img src="%s" alt="%s" loading="lazy">'%(esc(beat['path']),esc(block['heading'])) if beat else ''
            caption=('<em class="asset-boundary">%s · %s</em>'%('Explanatory graphic' if graphic else 'AI-generated contextual illustration · not a documentary photograph',esc(beat['truth_boundary']))) if beat else ''
            refs=' '.join('<a href="#source-%s">%s</a>'%(esc(ref),esc(ref)) for ref in p['evidence_refs'])
            result.append('<article class="scene %s" id="%s-part-%d" data-scene="%s">%s<div class="scene-copy"><small>%s · %02d / %02d</small><h2>%s</h2><p data-prose>%s</p><em>Evidence · %s</em>%s</div></article>'%(cls,esc(sid),n,esc(sid),image,esc(p['state']),n,len(bits),esc(block['heading']),esc(text),refs,caption))
        return ''.join(result)

    def route(key,title,blocks,ending=None):
        end=ending or {'text':'This route ends here. Choose another part of this connected world.'}
        body=''.join(scene(block,sid,by_scene.get(sid)) for sid,block in blocks)
        return '<section id="%s" class="route perspective-route" data-route="%s" hidden><header><a href="#perspectives">← Perspectives</a><span>%s</span></header>%s<section class="boundary route-end"><small>%s · PERSPECTIVE COMPLETE</small><h2>This route ends here.</h2><p>%s</p>%s<a class="route-exit" href="#perspectives">Choose what to explore next ↑</a></section></section>'%(esc(key),esc(key.removeprefix('route-')),esc(title),body,esc(title),esc(end['text']),end.get('extra',''))

    panels=[]; entries=[]
    for i,r in enumerate(routes,1):
        rid='route-'+r['perspective_id']
        blocks=[(s['scene_id'],copy['scenes'][s['scene_id']]) for s in r['scenes']]
        limits=''.join('<li>%s</li>'%esc(s['causal_boundary']) for s in r['scenes'] if s.get('causal_boundary'))
        purpose=r.get('purposeful_ending') or r.get('ending') or {}
        if isinstance(purpose,str): purpose={'label':'Explore further','text':purpose}
        purpose_html='<aside class="purposeful-ending"><small>%s</small><p>%s</p>%s</aside>'%(esc(purpose.get('label','A way forward')),esc(purpose.get('text','Inspect the evidence and follow the related people, places or organisations.')),('<a href="%s" rel="noopener">%s ↗</a>'%(esc(purpose['url']),esc(purpose.get('link_label','Explore')))) if purpose.get('url') else '')
        panels.append(route(rid,r['perspective'],blocks,{'text':'The evidence has limits. Follow the sources and choose what to explore next.','extra':purpose_html+'<details><summary>What the evidence can and cannot say</summary><ul>'+limits+'</ul></details>'}))
        asset=next((by_scene.get(s['scene_id']) for s in r['scenes'] if by_scene.get(s['scene_id']) and by_scene[s['scene_id']]['provider']!='ATLAS_DETERMINISTIC_GRAPHIC'),hero)
        entries.append('<a class="perspective" href="#%s" data-perspective="%s"><img src="%s" alt="" loading="lazy"><div class="perspective-copy"><b>%02d / %02d</b><h2>%s</h2><p>%s</p></div></a>'%(esc(rid),esc(r['perspective_id']),esc(asset['path']),i,len(routes),esc(r['perspective']),esc(r['scenes'][0]['meaning'])))
    shared=[]
    for key,title in [('reality','WHAT’S REAL'),('consequences','CONSEQUENCES'),('place','PLACE')]:
        shared.append(route(key,title,[(key+'-scene',copy['opening' if key=='reality' else key])]))
    story_text=''.join('<p>%s</p>'%esc(p) for p in story['story'])
    story_panel='<section id="story" class="route perspective-route" data-route="story" hidden><header><a href="#perspectives">← Perspectives</a><span>STORY / FICTION</span></header><section class="boundary"><small>STORY / FICTION</small><h2>%s</h2><p>%s</p><p>These people, dialogue and events are invented. This is not testimony.</p></section><div class="story-copy">%s</div><section class="boundary route-end"><a class="route-exit" href="#perspectives">Choose what to explore next ↑</a></section></section>'%(esc(story['title']),esc(story['boundary']),story_text)
    source_html=''.join('<details id="source-%s"><summary>%s · %s</summary><p>Supports: %s</p><p>Limit: %s</p><a href="%s" rel="noopener">Open source ↗</a></details>'%(esc(s['id']),esc(s['id']),esc(s['title']),esc(s['supports']),esc(s['limitation']),esc(s['url'])) for s in sources)
    menu='<nav class="edition-links"><a href="#reality">WHAT’S REAL</a> · <a href="#story">STORY / FICTION</a> · <a href="#consequences">CONSEQUENCES</a> · <a href="#place">PLACE</a> · <a href="#sources">SOURCES</a></nav>'
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#050708"><meta name="robots" content="noindex,nofollow"><title>%s · Atlasoquence</title><link rel="stylesheet" href="adaptive.css"><link rel="stylesheet" href="edition.css"><script src="adaptive.js" defer></script></head><body data-reader-family="aoc001-adaptive" data-opening-mode="%s"><main id="shell"><section class="hero video-entry" id="home"><img class="edition-geo-bg" src="%s" alt="%s · contextual illustration">%s<div class="shade"></div><div class="film-mark"><span>ATLASOQUENCE</span><span>%s</span></div><button class="skip-film" type="button">Skip opening ↓</button><div class="top reveal-copy"><span>ATLASOQUENCE</span><span>%s · READER TEST</span></div><div class="hero-copy reveal-copy"><div class="eyebrow">A CHANGING WORLD · MULTIPLE WAYS IN</div><h1>%s</h1><p>%s</p><a class="enter" href="#perspectives">Choose a perspective ↓</a></div></section><section id="perspectives" class="menu"><div class="menu-head"><span>PERSPECTIVES</span><p>%d perspectives. One connected world. Scroll, then choose where you want to enter.</p></div><div class="perspective-list">%s</div>%s</section>%s%s%s<section class="route sources" id="sources" hidden><header><a href="#perspectives">← Perspectives</a><span>SOURCES</span></header><div class="boundary"><h2>Inspect the evidence.</h2>%s<p>Facts can change the fiction. Fiction must never quietly become fact.</p></div></section></main></body></html>'''%(esc(candidate['working_title']),mode,esc(hero['path']),esc(candidate['geographic_core']),opening,esc(edition),esc(edition),esc(candidate['working_title']),esc(candidate.get('world_change') or routes[0]['scenes'][0]['meaning']),len(routes),''.join(entries),menu,''.join(panels),''.join(shared),story_panel,source_html)
    target=ROOT/'public/review'/edition.lower(); target.mkdir(parents=True,exist_ok=True)
    (target/'index.html').write_text(page,encoding='utf8')
    shutil.copyfile(CANONICAL/'adaptive.css',target/'adaptive.css')
    shutil.copyfile(ROOT/'public/review/adaptive.js',target/'adaptive.js')
    shutil.copyfile(ROOT/'public/review/edition.css',target/'edition.css')
    return target/'index.html'
