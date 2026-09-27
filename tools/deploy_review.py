#!/usr/bin/env python3
"""Deploy a pushed test-branch commit to the existing Render review service."""
import json, os, subprocess, sys, time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
SERVICE="srv-dase6m8jo6nc73bdh1ig"
BASE="https://atlas-automated-edition-test-1.onrender.com"
def git(*args): return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def api(path,key,body=None):
    request=Request("https://api.render.com/v1"+path,
                    data=json.dumps(body).encode() if body is not None else None,
                    headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},
                    method="POST" if body is not None else "GET")
    with urlopen(request,timeout=30) as response:return json.load(response)
def main(run):
    if git("branch","--show-current")!="test/automated-edition-1":raise RuntimeError("wrong branch")
    if git("status","--porcelain"):raise RuntimeError("commit assets and reader before deployment")
    sha=git("rev-parse","HEAD")
    if git("ls-remote","origin","refs/heads/test/automated-edition-1").split()[0]!=sha:
        raise RuntimeError("review branch commit has not been pushed")
    receipt=json.loads((run/"production-receipt.json").read_text())
    if receipt["defects"] or not receipt["reader"]: raise RuntimeError("production layers incomplete")
    key=os.environ.get("RENDER_API_KEY")
    if not key: raise RuntimeError("RENDER_API_KEY unavailable")
    task=api(f"/services/{SERVICE}/deploys",key,{"commitId":sha})
    deploy_id=task["id"]
    status=None
    for _ in range(50):
        data=api(f"/services/{SERVICE}/deploys/{deploy_id}",key)
        status=data.get("status")
        if status=="live":break
        if status in {"build_failed","update_failed","canceled","deactivated"}:break
        time.sleep(10)
    result={"edition_id":receipt["edition_id"],"branch":"test/automated-edition-1","commit":sha,
            "target":SERVICE,"deploy_id":deploy_id,"deployment_result":status,
            "base_url":BASE,"url":BASE+"/"+receipt["reader"].removeprefix("public/").removesuffix("index.html"),
            "asset_integration_status":"PASS","status":"PASS" if status=="live" else "BLOCKED"}
    (run/"deployment-receipt.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2));return status!="live"
if __name__=="__main__":
    try:sys.exit(main(Path(sys.argv[1])))
    except Exception as e:print("DEPLOY BLOCKED:",e,file=sys.stderr);sys.exit(1)
