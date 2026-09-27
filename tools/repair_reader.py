#!/usr/bin/env python3
"""Bounded CSS repair for rendered layout, crop and luminance defects only."""
import base64,json,os,re,sys
from pathlib import Path
from urllib.request import Request,urlopen
from production_state import read, write, reader_hashes

ROOT=Path(__file__).resolve().parents[1]
def main(run):
    key=os.environ.get("OPENAI_API_KEY")
    if not key:raise RuntimeError("OPENAI_API_KEY unavailable")
    candidate=json.loads((run/"selected-edition-candidate.json").read_text())
    css=ROOT/"public"/"review"/candidate["candidate_id"].lower()/"reader.css"
    dom=json.loads((run/"rendered-qa.json").read_text())
    visual=json.loads((run/"visual-review.json").read_text())
    allowed=("crop","dark","readab","typograph","overflow","off-centre","off-center","safe area","spacing","alignment","contrast","uniform")
    faults=dom["errors"]+[d for d in visual["defects"] if any(word in str(d).lower() for word in allowed)]
    if not faults:
        raise RuntimeError("defects require source, asset, editorial or evidence repair, not CSS")
    screenshot=(run/"screenshots"/"phone-edition.png").read_bytes()
    prompt=("Return ONLY a small CSS patch to repair these observed defects in the deployed Atlas reader: "
            +json.dumps(faults)+". Current CSS: "+css.read_text()[-16000:]
            +". Preserve every route, image, caption, source and FICTION boundary. "
             "Do not hide, remove, crop away or obscure content. Only adjust layout, object-position, brightness, "
             "spacing, contrast or typography. Do not include markdown fences or explanations.")
    payload={"model":os.environ.get("ATLAS_REPAIR_MODEL","gpt-4.1"),
             "input":[{"role":"user","content":[{"type":"input_text","text":prompt},
                  {"type":"input_image","image_url":"data:image/png;base64,"+base64.b64encode(screenshot).decode()}]}]}
    request=Request("https://api.openai.com/v1/responses",data=json.dumps(payload).encode(),
                    headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
    with urlopen(request,timeout=180) as res:data=json.load(res)
    patch="".join(p.get("text","") for x in data.get("output",[]) for p in x.get("content",[])).strip()
    if not patch or len(patch)>5000 or "{" not in patch or patch.count("{")!=patch.count("}"):
        raise RuntimeError("invalid CSS repair")
    if re.search(r'@import|url\s*\(|display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0\b|content\s*:',patch,re.I):
        raise RuntimeError("CSS repair would hide or fetch content")
    css.write_text(css.read_text()+"\n/* Automated rendered repair; verify again before release. */\n"+patch+"\n")
    receipt=read(run/'production-receipt.json')
    receipt['reader_hashes']=reader_hashes(css.parent/'index.html')
    write(run/'production-receipt.json',receipt)
    print("Reader CSS repair applied; deployment and visual QA must rerun")
if __name__=="__main__":
    try:main(Path(sys.argv[1]))
    except Exception as e:print("READER REPAIR BLOCKED:",e,file=sys.stderr);sys.exit(1)
