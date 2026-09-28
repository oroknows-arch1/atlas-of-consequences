#!/usr/bin/env python3
"""Independent multimodal visual review of deployed phone/desktop screenshots."""
import base64,json,os,sys,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from production_state import binding, read, write, require_current

def picture(path): return {"type":"input_image","image_url":"data:image/png;base64,"+base64.b64encode(path.read_bytes()).decode()}

OBJECT=lambda fields:{'type':'object','properties':fields,'required':list(fields),'additionalProperties':False}
VERDICT_SCHEMA=OBJECT({'status':{'type':'string','enum':['PASS','BLOCKED']},
  'defects':{'type':'array','items':OBJECT({'worker':{'type':'string'},'reason':{'type':'string'},'scene_id':{'type':'string'}})},
  'benchmark_parity':{'type':'string','enum':['PASS','BLOCKED']},'parity_reason':{'type':'string'}})

def ask_batch(files, key):
    names=[str(p) for p in files]
    prompt=("Independently inspect this batch of rendered publication screenshots. Files are in this order: "
            +json.dumps(names)+". benchmark-* images are AOC-001, a quality standard, not a template. "
            "Return ONLY JSON with keys status (PASS or BLOCKED), defects (array of objects with worker, reason, "
            "and scene_id if relevant), benchmark_parity (PASS or BLOCKED), and parity_reason. "
            "Worker must be reader_builder (navigation/structure), reader_treatment (crop, typography, darkness), "
            "visual_factory (context/continuity), asset_persistence (missing image), editorial_factory (copy), "
            "or source_registrar (source). Inspect every supplied image for crop, readable midtones, visual "
            "continuity/uniformity, typography, overflow, centering, safe areas, sources, FACT/STORY visibility, "
            "editorial depth and geographic specificity. Do not require the benchmark Perspective count, subjects, "
            "route sequence. The publication grammar IS required: full-screen cover imagery, overlaid restrained serif scene titles, image-led vertical Perspective discovery, low text density and cinematic entry. A conventional article, image-above-text stack, or link-card grid is BLOCKED even when readable. Compare candidate and benchmark at the same viewport. Explanatory graphics must remain fully readable; text-only boundary beats and sources can differ. Atlas permits clearly labelled AI-generated contextual illustrations; do not "
            "block solely because an image is AI-generated or non-documentary. Block only a scene-specific failure: "
            "generic or repeated treatment that loses the stated meaning/locality, misleading documentary implication, "
            "broken continuity, unreadability, missing content, or other required publication work. "
            "PASS requires zero defects. This is one batch of a complete inspection; do not assume unseen screenshots pass.")
    content=[{"type":"input_text","text":prompt}]+[picture(p) for p in files]
    models=[]
    for model in (os.environ.get("ATLAS_VISION_MODEL","gpt-4.1"),"gpt-4o-mini"):
        if model not in models: models.append(model)
    last_error=None
    for model in models:
        body={"model":model,"input":[{"role":"user","content":content}],
              "max_output_tokens":2000,
              "text":{"format":{"type":"json_schema","name":"atlas_rendered_review",
                                "strict":True,"schema":VERDICT_SCHEMA}}}
        request=Request("https://api.openai.com/v1/responses",data=json.dumps(body).encode(),
                        headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
        for attempt in range(1,4):
            try:
                with urlopen(request,timeout=180) as res: response=json.load(res)
                if response.get('status')!='completed':
                    raise RuntimeError('incomplete visual review: '+str(response.get('incomplete_details')))
                text="".join(p.get("text","") for x in response.get("output",[]) for p in x.get("content",[]))
                if not text:raise RuntimeError('empty visual review output')
                verdict=json.loads(text)
                if verdict.get("status") not in {"PASS","BLOCKED"} or verdict.get("benchmark_parity") not in {"PASS","BLOCKED"}:
                    raise RuntimeError("invalid visual review")
                if not isinstance(verdict.get("defects"),list) or any(not isinstance(d,dict) or not d.get("worker") or not d.get("reason") for d in verdict["defects"]):
                    raise RuntimeError("invalid structured visual defects")
                return verdict
            except HTTPError as error:
                last_error=error
                if error.code != 429 or attempt == 3: break
                retry_after=float(error.headers.get("Retry-After","0") or 0)
                time.sleep(min(60,max(attempt*15,retry_after)))
            except (json.JSONDecodeError, ValueError, RuntimeError) as error:
                last_error=error
                if attempt == 3: break
                time.sleep(2)
    if last_error: raise last_error
    raise RuntimeError("visual review provider returned no response")

def main(run):
    key=os.environ.get("OPENAI_API_KEY")
    if not key: raise RuntimeError("OPENAI_API_KEY unavailable")
    rendered=read(run/'rendered-qa.json'); deploy=read(run/'deployment-receipt.json'); require_current(run,rendered)
    shots=rendered.get('screenshots',[]); files=[run/s['path'] for s in shots]
    if not files or not any('benchmark-' in s['path'] and '-route-' in s['path'] for s in shots): raise RuntimeError('candidate views and actual benchmark routes required')
    benchmark=[p for p in files if 'benchmark-' in str(p)]
    candidate=[p for p in files if 'benchmark-' not in str(p)]
    batches=[candidate[i:i+4] for i in range(0,len(candidate),4)]
    # Every batch receives same-viewport canonical context, not only the first.
    batches=[batch+[p for p in benchmark if any(('phone-' in str(c) and 'phone-' in str(p)) or ('desktop-' in str(c) and 'desktop-' in str(p)) for c in batch) and any(k in str(p) for k in ('opening','identity','menu','route-0'))] for batch in batches]
    verdicts=[ask_batch(batch,key) for batch in batches]
    defects=[d for verdict in verdicts for d in verdict.get("defects",[])]
    status="PASS" if all(v["status"]=="PASS" for v in verdicts) and not defects else "BLOCKED"
    contract=read(run/'reader-contract-qa.json'); require_current(run,contract)
    if contract.get('reader_hashes')!=deploy['reader_hashes'] or contract.get('deploy_id')!=deploy['deploy_id']: raise RuntimeError('stale reader contract QA')
    parity="PASS" if status=='PASS' and contract['status']=='PASS' and all(v["benchmark_parity"]=="PASS" for v in verdicts) else "BLOCKED"
    parity_reason=" | ".join(v.get("parity_reason","") for v in verdicts)
    edition=json.loads((run/"selected-edition-candidate.json").read_text())["candidate_id"]
    common={**binding(run),"reader_hashes":deploy['reader_hashes'],"deploy_id":deploy['deploy_id'],"screenshots":shots}
    write(run/"visual-review.json",{**common,"status":status,"defects":defects})
    write(run/"benchmark-parity.json",{**common,"status":parity,"reason":parity_reason,"contract_version":contract["version"],"contract_status":contract["status"]})
    print(json.dumps({"status":status,"benchmark_parity":parity,"batches":len(batches),"defects":defects},indent=2))
    return status!="PASS" or parity!="PASS"

if __name__=="__main__":
    try: sys.exit(main(Path(sys.argv[1])))
    except Exception as e:
        print("RENDERED REVIEW BLOCKED:",e,file=sys.stderr); sys.exit(1)
