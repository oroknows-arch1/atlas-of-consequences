#!/usr/bin/env python3
"""Fail-closed publication production from gated editorial receipts.

An image provider is an executable command taking a JSON job on stdin and
returning JSON {"path": "/absolute/binary/path", "provider": "...", "provenance": "..."}.
It must itself generate/obtain the image; a prompt or temporary URL is not a result.
An independent visual verifier takes the same job plus `asset_path` on stdin
and returns {"pass": true, "reason": "..."}. Neither command may self-approve.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_GATES = ("selected-edition-gate", "story_plausibility_gate")

def read(path): return json.loads(path.read_text(encoding="utf8"))
def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf8")
def escape(s): return html.escape(str(s), quote=True)
def invoke(command, payload):
    result = subprocess.run(command, input=json.dumps(payload), text=True,
                            shell=True, capture_output=True, timeout=180)
    if result.returncode: raise RuntimeError(result.stderr.strip() or "provider exited unsuccessfully")
    return json.loads(result.stdout)

def facts(run, candidate):
    for name in REQUIRED_GATES:
        receipt=read(run/(name+".json"))
        if receipt.get("status")!="PASS": raise RuntimeError(f"{name} did not pass")
        identity=receipt.get("output",{}).get("candidate_id")
        if identity and identity!=candidate: raise RuntimeError(f"{name} belongs to {identity}, not {candidate}")
    names=("route_scene_generation", "causal_boundary_gate", "visual_requirements",
           "image_provider_routing", "story_synthesis", "story_plausibility_gate")
    receipts={n:read(run/(n+".json")) for n in names}
    for n,r in receipts.items():
        if r.get("status")!="PASS" or r.get("output",{}).get("candidate_id")!=candidate:
            raise RuntimeError(f"{n} missing PASS receipt for {candidate}")
    original=receipts["route_scene_generation"]["output"]["routes"]
    bounded=receipts["causal_boundary_gate"]["output"]["routes"]
    accepted_receipt=read(run/"selected-edition-perspectives.json")
    if accepted_receipt.get("status")!="PASS" or accepted_receipt.get("output",{}).get("candidate_id")!=candidate:
        raise RuntimeError("accepted Perspectives receipt missing or belongs to another candidate")
    accepted={p["id"] for p in accepted_receipt["output"]["perspectives"] if p["status"]=="ACCEPTED"}
    if {r["perspective_id"] for r in bounded}!=accepted:
        raise RuntimeError("reader routes do not match evidence-derived accepted Perspectives")
    if [(r["perspective_id"], [s["scene_id"] for s in r["scenes"]]) for r in original] != [(r["perspective_id"], [s["scene_id"] for s in r["scenes"]]) for r in bounded]:
        raise RuntimeError("bounded route topology differs from accepted route topology")
    requirements=receipts["visual_requirements"]["output"]["requirements"]
    routed=receipts["image_provider_routing"]["output"]["visuals"]
    if {v["scene_id"] for v in routed}!={v["scene_id"] for v in requirements}:
        raise RuntimeError("visual routing and requirements refer to different scenes")
    for v in requirements:
        if v["required"] != next(x for x in routed if x["scene_id"]==v["scene_id"])["required"]:
            raise RuntimeError(f"{v['scene_id']}: requirement changed during routing")
    return bounded, requirements, receipts["story_synthesis"]["output"]

def validate_binary(path, contextual):
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        if min(image.size)<600: raise RuntimeError("image resolution below 600px")
        if contextual:
            gray=image.convert("L").resize((100,100))
            brightness=ImageStat.Stat(gray).mean[0]
            if brightness<48: raise RuntimeError(f"image too dark ({brightness:.1f})")

def make_graphic(path, scene, requirement, source_ids, datum):
    # Source-labelled explanatory image with explicit scope; no invented map data.
    import textwrap
    if not datum or not datum.get("value") or not datum.get("scope") or not datum.get("source_id") in source_ids:
        raise RuntimeError("deterministic graphic lacks verified value, scope or scene source")
    title=datum["caption"]
    lines=textwrap.wrap(title, width=38)
    body="".join(f'<text x="90" y="{440+i*58}" font-size="42" fill="#f3eadb">{escape(line)}</text>' for i,line in enumerate(lines))
    caption=escape("Scope: "+datum["scope"]+" · Source: "+datum["source_id"])
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><rect width="1600" height="900" fill="#15252a"/><path d="M80 225 H1520" stroke="#d5874a" stroke-width="5"/><text x="90" y="115" font-family="sans-serif" font-size="27" letter-spacing="5" fill="#ecb98c">ATLASOQUENCE · EXPLANATORY</text><text x="90" y="350" font-family="Georgia,serif" font-size="118" fill="#f3eadb">{escape(datum['value'])}</text><g font-family="Georgia,serif">{body}</g><text x="90" y="820" font-family="sans-serif" font-size="25" fill="#e2dccf">{caption}</text></svg>'''
    # SVG is a persistent image binary, but it must carry actual explanation, not a gradient substitute.
    path.write_bytes(svg.encode("utf8"))

def produce_assets(run, edition, routes, requirements, output):
    generator=os.environ.get("ATLAS_IMAGE_COMMAND")
    verifier=os.environ.get("ATLAS_VISUAL_QA_COMMAND")
    asset_dir=ROOT/"public"/"assets"/edition.lower()
    asset_dir.mkdir(parents=True,exist_ok=True)
    scenes={s["scene_id"]:s for r in routes for s in r["scenes"]}
    context_file=run/"visual-context.json"
    if not context_file.exists():
        return [],[{"worker":"visual_factory","reason":"geographic/cultural visual context receipt missing"}]
    context=read(context_file)
    graphic_data=read(run/"visual-data.json") if (run/"visual-data.json").exists() else {}
    if context.get("candidate_id")!=edition or not context.get("locality_evidence"):
        return [],[{"worker":"visual_factory","reason":"visual context is not evidenced for this edition"}]
    assets=[]; defects=[]
    for spec in requirements:
        if not spec["required"]: continue
        sid=spec["scene_id"]
        scene=scenes[sid]
        contextual="deterministic" not in spec["visual_type"].lower()
        dest=asset_dir/(sid.lower()+(".png" if contextual else ".svg"))
        job={"edition_id":edition,"scene_id":sid,"meaning":scene["meaning"],
             "evidence_refs":scene["evidence_refs"],"truth_boundary":spec["truth_boundary"],
             "geography":output["geographic_core"],
             "visual_type":spec["visual_type"],"purpose":spec["purpose"],
             "fiction_status":"FACT_CONTEXTUAL", "continuity":context.get("visual_bible",{}),
             "locality_evidence":context["locality_evidence"],
             "style":"grounded editorial documentary, natural daylight, coherent warm-neutral grade; no text, identifiable signage or claimed event"}
        try:
            if contextual:
                if not generator or not verifier: raise RuntimeError("image generator and independent visual verifier commands are required")
                for attempt in range(1,4):
                    try:
                        result=invoke(generator,dict(job,attempt=attempt))
                        source=Path(result["path"])
                        if not source.is_file(): raise RuntimeError("provider returned no binary")
                        with Image.open(source) as im:
                            if im.format!="PNG": raise RuntimeError("image provider must return PNG")
                        validate_binary(source,True)
                        check=invoke(verifier,dict(job,asset_path=str(source),provider=result.get("provider")))
                        if check.get("pass") is not True: raise RuntimeError("visual/evidence QA: "+check.get("reason","failed"))
                        shutil.copyfile(source,dest)
                        break
                    except Exception:
                        if attempt==3: raise
            else:
                make_graphic(dest,scene,spec,scene["evidence_refs"],graphic_data.get(sid))
                result={"provider":"ATLAS_DETERMINISTIC_GRAPHIC","provenance":"scene meaning and evidence refs"}
            binary=dest.read_bytes()
            if not binary: raise RuntimeError("empty binary")
            assets.append({"scene_id":sid,"path":"/assets/"+edition.lower()+"/"+dest.name,
                           "sha256":hashlib.sha256(binary).hexdigest(),"bytes":len(binary),
                           "provenance":result.get("provenance"),"provider":result.get("provider"),
                           "truth_boundary":spec["truth_boundary"],"status":"PASS"})
        except Exception as exc:
            defects.append({"worker":"visual_factory" if contextual else "asset_persistence", "scene_id":sid,"reason":str(exc)})
    write(run/"asset-persistence-receipt.json",{"edition_id":edition,"status":"PASS" if not defects else "BLOCKED","assets":assets,"defects":defects})
    return assets,defects

def build_reader(run, edition, candidate, routes, story, assets):
    by_scene={x["scene_id"]:x for x in assets}
    source_file=run/"source-register.json"
    if not source_file.exists(): raise RuntimeError("structured source register missing")
    sources=read(source_file)
    if not sources or any(not x.get("url") or not x.get("id") for x in sources): raise RuntimeError("source register incomplete")
    refs={x["id"] for x in sources}
    for route in routes:
        for scene in route["scenes"]:
            if set(scene.get("evidence_refs",[]))-refs: raise RuntimeError(f"{scene['scene_id']}: source ID lacks register entry")
    navigation=''.join(f'<a href="#route-{escape(r["perspective_id"])}">{escape(r["perspective"])}</a>' for r in routes)
    panels=[]
    for route in routes:
        sections=[]
        for scene in route["scenes"]:
            asset=by_scene.get(scene["scene_id"])
            media=f'<figure><img src="{escape(asset["path"])}" alt="{escape(scene["meaning"])}" loading="lazy"><figcaption>{escape(asset["truth_boundary"])} · Contextual/explanatory visual</figcaption></figure>' if asset else ''
            citations=''.join(f'<a href="#source-{escape(ref)}">{escape(ref)}</a> ' for ref in scene.get("evidence_refs",[]))
            sections.append(f'<section class="scene" id="{escape(scene["scene_id"])}">{media}<div class="scene-copy"><small>{escape(scene["state"])} · {escape(scene["scene_id"] )}</small><h3>{escape(scene["meaning"])}</h3><p>{escape(scene["causal_boundary"])}</p><p class="refs">{citations}</p></div></section>')
        panels.append(f'<section class="route" id="route-{escape(route["perspective_id"])}"><nav><a href="#perspectives">← Perspectives</a><span>{escape(route["perspective"])}</span></nav><h2>{escape(route["perspective"])}</h2>{"".join(sections)}<footer><b>{escape(route["perspective"])} · ROUTE COMPLETE</b><p>Choose what to explore next.</p><a href="#perspectives">Choose a Perspective ↑</a></footer></section>')
    story_paragraphs=''.join(f'<p>{escape(p)}</p>' for p in story["story"])
    source_cards=''.join(f'<details id="source-{escape(x["id"])}"><summary>{escape(x["id"])} · {escape(x["title"])}</summary><p>{escape(x["supports"])}</p><p>Limit: {escape(x["limitation"])}</p><a href="{escape(x["url"])}" rel="noopener">Open source ↗</a></details>' for x in sources)
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#101719"><title>{escape(candidate['working_title'])} · Atlasoquence</title><link rel="stylesheet" href="reader.css"></head><body><main><header class="hero"><div class="top"><b>ATLASOQUENCE</b><span>{escape(edition)} · PUBLICATION CANDIDATE</span></div><div class="hero-copy"><small>{escape(candidate['geographic_core'])} · WORLD CHANGE</small><h1>{escape(candidate['working_title'])}</h1><p>{escape(candidate['world_change'])}</p><a href="#perspectives">Choose a Perspective ↓</a></div></header><section class="menu" id="perspectives"><small>PERSPECTIVES</small><h2>One change. Choose your way in.</h2><p>Each route ends deliberately. Your next choice is yours.</p><div class="cards">{navigation}</div></section>{''.join(panels)}<section class="story" id="story"><div class="story-inner"><small>STORY / FICTION</small><h2>{escape(story['title'])}</h2><p class="boundary">{escape(story['boundary'])}</p>{story_paragraphs}<aside><b>FICTION BOUNDARY</b><p>The named people, dialogue and household events are invented. They are not testimony or documented cases.</p></aside></div></section><section class="sources" id="sources"><small>WHAT'S REAL · SOURCES</small><h2>Inspect the evidence.</h2>{source_cards}<p>Facts can change the fiction. Fiction must never quietly become fact.</p></section></main></body></html>'''
    target=ROOT/"public"/"review"/edition.lower()
    target.mkdir(parents=True,exist_ok=True)
    (target/"index.html").write_text(page,encoding="utf8")
    shutil.copyfile(ROOT/"public"/"review"/"reader-production.css",target/"reader.css")
    return target/"index.html"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("run_dir",type=Path)
    args=ap.parse_args()
    run=args.run_dir.resolve()
    candidate=read(run/"selected-edition-candidate.json")
    edition=candidate["candidate_id"]
    defects=[]; assets=[]; reader=None
    try:
        routes,requirements,story=facts(run,edition)
        assets,defects=produce_assets(run,edition,routes,requirements,candidate)
        if not defects: reader=build_reader(run,edition,candidate,routes,story,assets)
    except Exception as exc: defects.append({"worker":"production_orchestrator","reason":str(exc)})
    receipt={"edition_id":edition,"state":"ASSEMBLED" if reader and not defects else "BLOCKED", "assets_persisted":len(assets),
             "reader":str(reader.relative_to(ROOT)) if reader else None,"defects":defects,
             "next_stage":"rendered_qa" if reader else "repair", "publication_authorized":False}
    write(run/"production-receipt.json",receipt)
    print(json.dumps(receipt,indent=2))
    return 0 if reader and not defects else 1

if __name__=="__main__": sys.exit(main())
