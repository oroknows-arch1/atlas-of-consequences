#!/usr/bin/env python3
"""Independent multimodal visual review of deployed phone/desktop screenshots."""
import base64,json,os,sys
from pathlib import Path
from urllib.request import Request,urlopen
from production_state import binding, read, write, require_current

def picture(path):return {"type":"input_image","image_url":"data:image/png;base64,"+base64.b64encode(path.read_bytes()).decode()}
def main(run):
    key=os.environ.get("OPENAI_API_KEY")
    if not key:raise RuntimeError("OPENAI_API_KEY unavailable")
    rendered=read(run/'rendered-qa.json')
    deploy=read(run/'deployment-receipt.json')
    require_current(run,rendered)
    shots=rendered.get('screenshots',[])
    files=[run/s['path'] for s in shots]
    if not files or not any('benchmark-route-' in s['path'] for s in shots):
        raise RuntimeError('candidate views and actual benchmark routes required')
    prompt=("Independently inspect these rendered publication screenshots. Files are in this order: "
            +json.dumps([s['path'] for s in shots])+". benchmark-* images are AOC-001, a quality standard, not a template. "
            "Return ONLY JSON with keys status (PASS or BLOCKED), defects (array of objects with worker, reason, "
            "and scene_id if relevant), benchmark_parity (PASS or BLOCKED), and parity_reason. "
            "Worker must be reader_builder (navigation/structure), reader_treatment (crop, typography, darkness), "
            "visual_factory (context/continuity), asset_persistence (missing image), editorial_factory (copy), "
            "or source_registrar (source). Inspect every route and shared section on phone and desktop. "
            "Judge crop, readable midtones, visual continuity/uniformity, typography, overflow, centering, "
            "safe areas, sources, FACT/STORY visibility, editorial depth and geographic specificity. "
            "Do not require the benchmark Perspective count, subjects, route sequence or media structure. "
            "Block thin content, generic visuals or any required publication work. PASS requires zero defects.")
    content=[{"type":"input_text","text":prompt}]+[picture(p) for p in files]
    body={"model":os.environ.get("ATLAS_VISION_MODEL","gpt-4.1"),"input":[{"role":"user","content":content}]}
    request=Request("https://api.openai.com/v1/responses",data=json.dumps(body).encode(),
                    headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
    with urlopen(request,timeout=180) as res:response=json.load(res)
    text="".join(p.get("text","") for x in response.get("output",[]) for p in x.get("content",[]))
    verdict=json.loads(text)
    if verdict.get("status") not in {"PASS","BLOCKED"} or verdict.get("benchmark_parity") not in {"PASS","BLOCKED"}:
        raise RuntimeError("invalid visual review")
    edition=json.loads((run/"selected-edition-candidate.json").read_text())["candidate_id"]
    if not isinstance(verdict.get('defects'),list) or any(not isinstance(d,dict) or not d.get('worker') or not d.get('reason') for d in verdict.get('defects',[])):
        raise RuntimeError('invalid structured visual defects')
    if verdict.get('defects') and verdict['status']=='PASS': verdict['status']='BLOCKED'
    common={**binding(run),'reader_hashes':deploy['reader_hashes'],'deploy_id':deploy['deploy_id'],'screenshots':shots}
    (run/"visual-review.json").write_text(json.dumps({**common,"status":verdict["status"],"defects":verdict["defects"]},indent=2)+"\n")
    (run/"benchmark-parity.json").write_text(json.dumps({**common,"status":verdict["benchmark_parity"],"reason":verdict["parity_reason"]},indent=2)+"\n")
    print(json.dumps(verdict,indent=2));return verdict["status"]!="PASS" or verdict["benchmark_parity"]!="PASS"
if __name__=="__main__":
    try:sys.exit(main(Path(sys.argv[1])))
    except Exception as e:print("RENDERED REVIEW BLOCKED:",e,file=sys.stderr);sys.exit(1)
