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
    source_by_id={s['id']:s for s in sources}
    selected={p['id']:p for p in read(run/'selected-edition-perspectives.json')['output']['perspectives']}
    display_file=run/'reader-display-copy.json'
    display=read(display_file) if display_file.exists() else {'edition_id':edition,'scene_overrides':{}}
    if display['edition_id']!=edition: raise ValueError('display copy belongs to another edition')
    overrides=display['scene_overrides']
    if set(overrides)-set(copy['scenes']): raise ValueError('display copy names an unknown scene')
    for sid,override in overrides.items():
        original=copy['scenes'][sid]
        if not override.get('heading') or len(override['paragraphs'])!=len(original['paragraphs']):
            raise ValueError('display copy changes scene structure: '+sid)
        for new,old in zip(override['paragraphs'],original['paragraphs']):
            if (new['state']!=old['state'] or new['evidence_refs']!=old['evidence_refs'] or
                len(chunks(new['text']))!=len(chunks(old['text']))):
                raise ValueError('display copy changes truth, evidence or beat coverage: '+sid)
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

    def scene(block, sid, asset, contextual):
        bits=[]
        for p in block['paragraphs']:
            if p['state'] not in ('FACT','UNCERTAIN','STORY') or set(p['evidence_refs'])-source_ids:
                raise ValueError('unverified truth state or evidence reference')
            bits.extend((p,t) for t in chunks(p['text']))
        result=[]
        for n,(p,text) in enumerate(bits,1):
            beat=by_beat.get(f'{sid}-B{n}') or asset
            # A structural preview may repeat a verified image; it never calls
            # that repetition finished visual coverage or publication evidence.
            if not beat and structural: beat=asset or hero
            graphic=beat['provider']=='ATLAS_DETERMINISTIC_GRAPHIC'
            visual=contextual[(n-1)%len(contextual)] if graphic else beat
            cls='scene-overlay'
            image='<img src="%s" alt="%s" loading="lazy">'%(esc(visual['path']),esc(block['heading']))
            caption='<em class="asset-boundary">AI-generated contextual illustration · not a documentary photograph · %s</em>'%esc(visual['truth_boundary'])
            if graphic:
                caption+='<a class="graphic-evidence" href="%s" rel="noopener" target="_blank" data-graphic-path="%s">Inspect verified explanatory graphic ↗</a><em class="asset-boundary">%s</em>'%(esc(beat['path']),esc(beat['path']),esc(beat['truth_boundary']))
            refs=' '.join('<a href="#source-%s">%s</a>'%(esc(ref),esc(ref)) for ref in p['evidence_refs'])
            if not beat: raise ValueError('scene has no verified visual: '+sid)
            heading='<h2>%s</h2>'%esc(block['heading']) if n==1 else ''
            result.append('<article class="scene %s" id="%s-part-%d" data-scene="%s">%s<div class="scene-copy"><small>%s · %02d / %02d</small>%s<p data-prose>%s</p><em>Evidence · %s</em>%s</div></article>'%(cls,esc(sid),n,esc(sid),image,esc(p['state']),n,len(bits),heading,esc(text),refs,caption))
        return ''.join(result)

    def route(key,title,blocks,ending=None):
        end=ending or {'text':'This route ends here. Choose another part of this connected world.'}
        scene_ids={sid for sid,_ in blocks}
        contextual=[a for a in available if a['scene_id'] in scene_ids and a['provider']!='ATLAS_DETERMINISTIC_GRAPHIC']
        if not contextual and structural: contextual=[hero]
        if not contextual: raise ValueError('route lacks verified contextual visual: '+key)
        body=''.join(scene(block,sid,by_scene.get(sid),contextual) for sid,block in blocks)
        return '<section id="%s" class="route perspective-route" data-route="%s" hidden><header><a href="#perspectives">← Perspectives</a><span>%s</span></header>%s<section class="boundary route-end"><small>%s · PERSPECTIVE COMPLETE</small><h2>This route ends here.</h2><p>%s</p>%s<a class="route-exit" href="#perspectives">Choose what to explore next ↑</a></section></section>'%(esc(key),esc(key.removeprefix('route-')),esc(title),body,esc(title),esc(end['text']),end.get('extra',''))

    panels=[]; entries=[]
    for i,r in enumerate(routes,1):
        rid='route-'+r['perspective_id']
        blocks=[(s['scene_id'],overrides.get(s['scene_id'],copy['scenes'][s['scene_id']])) for s in r['scenes']]
        limits=''.join('<li>%s</li>'%esc(s['causal_boundary']) for s in r['scenes'] if s.get('causal_boundary'))
        first_ref=next((ref for s in r['scenes'] for ref in s.get('evidence_refs',[]) if ref in source_ids),None)
        accepted=selected.get(r['perspective_id'])
        if accepted:
            source_id=next((ref for ref in accepted.get('evidence_basis',[]) if ref in source_by_id),None)
            if not source_id or not accepted.get('purpose'):
                raise ValueError('Perspective ending lacks accepted purpose or source: '+rid)
            source=source_by_id[source_id]
            sourced_purpose={'label':'Follow this Perspective into the evidence',
                'text':accepted['purpose'], 'url':source['url'],
                'link_label':source['title'], 'source_id':source_id}
        elif structural:
            sourced_purpose={'label':'Preview the evidence','text':'Inspect the source and its limits.',
                'url':'#source-'+first_ref if first_ref else '#sources','link_label':first_ref or 'Sources'}
        else:raise ValueError('Perspective lacks accepted edition purpose: '+rid)
        purpose=r.get('purposeful_ending') or r.get('ending') or sourced_purpose
        if isinstance(purpose,str): purpose={'label':'Explore further','text':purpose}
        purpose_html='<aside class="purposeful-ending" data-source-id="%s"><small>%s</small><p>%s</p>%s</aside>'%(esc(purpose.get('source_id','')),esc(purpose.get('label','A way forward')),esc(purpose.get('text','Inspect the evidence and follow the related people, places or organisations.')),('<a href="%s" rel="noopener">%s ↗</a>'%(esc(purpose['url']),esc(purpose.get('link_label','Explore')))) if purpose.get('url') else '')
        panels.append(route(rid,r['perspective'],blocks,{'text':'The evidence has limits. Follow the sources and choose what to explore next.','extra':purpose_html+'<details><summary>What the evidence can and cannot say</summary><ul>'+limits+'</ul></details>'}))
        asset=next((by_scene[s['scene_id']] for s in r['scenes'] if s['scene_id'] in by_scene and by_scene[s['scene_id']]['provider']!='ATLAS_DETERMINISTIC_GRAPHIC'),None)
        if not asset:
            asset=next((by_beat[f'{s["scene_id"]}-B1'] for s in r['scenes']
                        if f'{s["scene_id"]}-B1' in by_beat and by_beat[f'{s["scene_id"]}-B1']['provider']!='ATLAS_DETERMINISTIC_GRAPHIC'),None)
        if not asset:asset=hero
        entries.append((asset,r,rid))
    # The AOC-001 menu owns one continuous image surface and sibling hotspots.
    # Its artwork is edition data: verified stills and labels form a compact
    # contiguous surface, while the inherited hotspot/controller code runs it.
    teasers=[]; seen_teasers=set()
    for asset,r,rid in entries:
        teaser=next((s['meaning'] for s in r['scenes'] if s['meaning'] not in seen_teasers),None)
        if not teaser: raise ValueError('Perspective lacks a distinct verified menu teaser: '+rid)
        seen_teasers.add(teaser)
        teasers.append(teaser)
    slices=''.join('<div class="edition-menu-slice"><img src="%s" alt="" loading="lazy"><div class="edition-menu-label"><b>%02d / %02d</b><strong>%s</strong><span>%s</span></div></div>'%(esc(asset['path']),i,len(entries),esc(r['perspective']),esc(teasers[i-1])) for i,(asset,r,rid) in enumerate(entries,1))
    hotspots=''.join('<a class="perspective-hotspot" style="top:%s%%;height:%s%%" href="#%s" data-perspective="%s" aria-label="Enter %s perspective"></a>'%(100*i/len(entries),100/len(entries),esc(rid),esc(r['perspective_id']),esc(r['perspective'])) for i,(asset,r,rid) in enumerate(entries))
    shared=[]
    for key,title in [('reality','WHAT’S REAL'),('consequences','CONSEQUENCES'),('place','PLACE')]:
        shared.append(route(key,title,[(key+'-scene',copy['opening' if key=='reality' else key])]))
    story_text=''.join('<p>%s</p>'%esc(p) for p in story['story'])
    story_panel='<section id="story" class="route perspective-route" data-route="story" hidden><header><a href="#perspectives">← Perspectives</a><span>STORY / FICTION</span></header><section class="boundary"><small>STORY / FICTION</small><h2>%s</h2><p>%s</p><p>These people, dialogue and events are invented. This is not testimony.</p></section><div class="story-copy">%s</div><section class="boundary route-end"><a class="route-exit" href="#perspectives">Choose what to explore next ↑</a></section></section>'%(esc(story['title']),esc(story['boundary']),story_text)
    source_html=''.join('<details id="source-%s"><summary>%s · %s</summary><p>Supports: %s</p><p>Limit: %s</p><a href="%s" rel="noopener">Open source ↗</a></details>'%(esc(s['id']),esc(s['id']),esc(s['title']),esc(s['supports']),esc(s['limitation']),esc(s['url'])) for s in sources)
    menu='<nav class="edition-links"><a href="#reality">WHAT’S REAL</a> · <a href="#story">STORY / FICTION</a> · <a href="#consequences">CONSEQUENCES</a> · <a href="#place">PLACE</a> · <a href="#sources">SOURCES</a></nav>'
    deck=candidate.get('hero_deck') or routes[0]['scenes'][0]['meaning']
    if len(deck.split())>28: raise ValueError('opening deck exceeds canonical reader pacing')
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#050708"><meta name="robots" content="noindex,nofollow"><title>%s · Atlasoquence</title><link rel="stylesheet" href="adaptive.css"><link rel="stylesheet" href="edition.css"><script src="adaptive.js" defer></script></head><body data-reader-family="aoc001-adaptive" data-opening-mode="%s"><main id="shell"><section class="hero video-entry" id="home"><img class="edition-geo-bg" src="%s" alt="%s · contextual illustration">%s<div class="shade"></div><div class="film-mark"><span>ATLASOQUENCE</span><span>%s</span></div><button class="skip-film" type="button">Skip opening ↓</button><div class="top reveal-copy"><span>ATLASOQUENCE</span><span>%s · READER TEST</span></div><div class="hero-copy reveal-copy"><div class="eyebrow">A CHANGING WORLD · MULTIPLE WAYS IN</div><h1>%s</h1><p>%s</p><a class="enter" href="#perspectives">Choose a perspective ↓</a></div></section><section id="perspectives" class="menu visual-perspective-menu"><div class="menu-head"><span>PERSPECTIVES</span><p>%d perspectives. One connected world. Scroll, then choose where you want to enter.</p></div><div class="perspective-menu-image"><div class="edition-menu-art">%s</div>%s</div>%s</section>%s%s%s<section class="route perspective-route sources" id="sources" data-route="sources" hidden><header><a href="#perspectives">← Perspectives</a><span>SOURCES</span></header><div class="boundary"><h2>Inspect the evidence.</h2>%s<p>Facts can change the fiction. Fiction must never quietly become fact.</p></div></section></main></body></html>'''%(esc(candidate['working_title']),mode,esc(hero['path']),esc(candidate['geographic_core']),opening,esc(edition),esc(edition),esc(candidate['working_title']),esc(deck),len(routes),slices,hotspots,menu,''.join(panels),''.join(shared),story_panel,source_html)
    target=ROOT/'public/review'/edition.lower(); target.mkdir(parents=True,exist_ok=True)
    (target/'index.html').write_text(page,encoding='utf8')
    shutil.copyfile(CANONICAL/'adaptive.css',target/'adaptive.css')
    shutil.copyfile(ROOT/'public/review/adaptive.js',target/'adaptive.js')
    shutil.copyfile(ROOT/'public/review/edition.css',target/'edition.css')
    return target/'index.html'
