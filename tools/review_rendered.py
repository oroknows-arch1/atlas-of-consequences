#!/usr/bin/env python3
"""Independent multimodal visual review of deployed phone/desktop screenshots."""
import base64,json,os,sys
from pathlib import Path
from urllib.request import Request,urlopen

def picture(path):return {"type":"input_image","image_url":"data:image/png;base64,"+base64.b64encode(path.read_bytes()).decode()}
def main(run):
    key=os.environ.get("OPENAI_API_KEY")
    if not key:raise RuntimeError("OPENAI_API_KEY unavailable")
    screenshots=run/"screenshots"
    files=[screenshots/"phone.png",screenshots/"desktop.png",screenshots/"benchmark-phone.png"]
    if any(not p.is_file() for p in files):raise RuntimeError("candidate and AOC-001 benchmark screenshots required")
    prompt=("Inspect the first TWO full-page screenshots of a deployed Atlas edition at phone and desktop widths. "
            "The THIRD screenshot is AOC-001, a quality benchmark, not a structural template. "
            "Return ONLY JSON with keys status ('PASS' or 'BLOCKED'), defects (array of specific visual defects), "
            "benchmark_parity ('PASS' or 'BLOCKED'), and parity_reason. "
            "Assess actual rendered images, crop, darkness and readability, visual continuity and uniformity, typography, "
            "overflow, centering, safe areas, image/text relationship, sources, FACT/STORY visibility, navigation, "
            "editorial depth and contextual specificity. Do not demand the same Perspective count, geography, "
            "characters, media structure or route order as AOC-001. Fail if any material defect remains. "
            "Screenshots cannot verify deployed asset bytes or navigation behaviour; those have separate gates.")
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
    (run/"visual-review.json").write_text(json.dumps({"edition_id":edition,"status":verdict["status"],"defects":verdict["defects"]},indent=2)+"\n")
    (run/"benchmark-parity.json").write_text(json.dumps({"edition_id":edition,"status":verdict["benchmark_parity"],"reason":verdict["parity_reason"]},indent=2)+"\n")
    print(json.dumps(verdict,indent=2));return verdict["status"]!="PASS" or verdict["benchmark_parity"]!="PASS"
if __name__=="__main__":
    try:sys.exit(main(Path(sys.argv[1])))
    except Exception as e:print("RENDERED REVIEW BLOCKED:",e,file=sys.stderr);sys.exit(1)
