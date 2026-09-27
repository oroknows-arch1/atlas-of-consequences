#!/usr/bin/env python3
"""Repository-owned image generation adapter. Reads one scene job from stdin."""
import base64, json, os, sys, tempfile
from urllib.request import Request, urlopen
from provider_errors import describe

def main():
    job=json.load(sys.stdin)
    key=os.environ.get("OPENAI_API_KEY")
    if not key: raise RuntimeError("OPENAI_API_KEY unavailable")
    prompt=(f"Create one grounded editorial contextual photograph for an Atlas publication. "
            f"Geography: {job['geography']}. Scene meaning: {job['meaning']}. "
            f"Visual purpose: {job['purpose']}. Truth boundary: {job['truth_boundary']}. "
            f"Local context, with source scope: {json.dumps(job['locality_evidence'])}. "
            f"Continuity rules: {json.dumps(job['continuity'])}. "
            "This is a representative scene, not a photograph of a documented event, identified worker, school or factory. "
            "No visible text, logos or invented signage. No melodrama. Natural light, clear midtones, 3:2 wide composition. "
            f"Revision attempt {job.get('attempt',1)}. Fix this previous visual QA failure: {job.get('repair_feedback') or 'none'}.")
    if job.get('safe_composition'):
        prompt=("Create a grounded editorial illustration of an ordinary environment. "
                +job['safe_composition']+". No people, bodies, distress, injury or reenactment. "
                +f"Geography: {job['geography']}. Editorial meaning: {job['meaning']}. "
                +f"Purpose: {job['purpose']}. Boundary: {job['truth_boundary']}. "
                +f"Visual continuity: {json.dumps(job['continuity'])}. "
                +"Natural daylight, readable midtones, 3:2 composition. No text or logos. "
                +"Representative contextual illustration, not evidence of a specific event or site.")
    body=json.dumps({"model":os.environ.get("ATLAS_IMAGE_MODEL","gpt-image-1"),
                     "prompt":prompt,"size":"1536x1024","quality":"medium","output_format":"png","n":1}).encode()
    request=Request("https://api.openai.com/v1/images/generations",data=body,
                    headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
    with urlopen(request,timeout=150) as response: result=json.load(response)
    binary=base64.b64decode(result["data"][0]["b64_json"])
    with tempfile.NamedTemporaryFile(prefix="atlas-scene-",suffix=".png",delete=False) as f:
        f.write(binary);path=f.name
    print(json.dumps({"path":path,"provider":os.environ.get("ATLAS_IMAGE_MODEL","gpt-image-1"),
                      "provenance":"generated representative editorial scene from bounded visual job "+job["scene_id"]}))
if __name__=="__main__":
    try: main()
    except Exception as e: print(describe(e),file=sys.stderr);sys.exit(1)
