#!/usr/bin/env python3
"""Independent image inspection adapter; does not produce or edit the asset."""
import base64,json,os,sys
from pathlib import Path
from urllib.request import Request,urlopen
from provider_errors import describe

def main():
    job=json.load(sys.stdin)
    key=os.environ.get("OPENAI_API_KEY")
    if not key: raise RuntimeError("OPENAI_API_KEY unavailable")
    binary=Path(job["asset_path"]).read_bytes()
    data="data:image/png;base64,"+base64.b64encode(binary).decode()
    instruction=("Independently inspect this proposed Atlas contextual visual. Return ONLY JSON "
                 "{\"pass\": boolean, \"reason\": string}. Fail if it is a collage, generic unrelated image, "
                 "visibly wrong for the geography, misleadingly specific, poor quality, dark, cropped badly, "
                 "contains signs/text suggesting a documented site, or contradicts the visual purpose. "
                 "This is generated contextual illustration, displayed with the explicit caption "
                 "AI-generated contextual illustration — not a documentary photograph. It is not submitted "
                 "as evidence that an event happened. Do not fail solely because it is generated or cannot "
                 "prove a real event. Still FAIL misleading specificity, invented identifiable institutions, "
                 "staged distress, implausible anatomy, stylized/unnatural faces or environments, weak "
                 "continuity, and every quality or evidence-boundary defect listed above. "
                 f"Scene: {job['meaning']}. Location: {job['geography']}. Purpose: {job['purpose']}. "
                 f"Truth boundary: {job['truth_boundary']}. Context: {json.dumps(job['locality_evidence'])}. "
                 f"Continuity: {json.dumps(job['continuity'])}.")
    payload={"model":os.environ.get("ATLAS_VISION_MODEL","gpt-4.1"),
             "input":[{"role":"user","content":[{"type":"input_text","text":instruction},
                     {"type":"input_image","image_url":data}]}]}
    request=Request("https://api.openai.com/v1/responses",data=json.dumps(payload).encode(),
                    headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
    with urlopen(request,timeout=120) as response: result=json.load(response)
    text="".join(part.get("text","") for item in result.get("output",[]) for part in item.get("content",[]))
    verdict=json.loads(text)
    if type(verdict.get("pass")) is not bool or not verdict.get("reason"): raise RuntimeError("invalid independent QA verdict")
    print(json.dumps(verdict))
if __name__=="__main__":
    try: main()
    except Exception as e: print(describe(e),file=sys.stderr);sys.exit(1)
