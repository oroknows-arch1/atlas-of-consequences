#!/usr/bin/env python3
"""Deploy a pushed test-branch commit to the existing Render review service."""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path
from urllib.request import Request, urlopen
from production_state import binding, require_current, reader_hashes

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
    if git("status","--porcelain","--","public"):raise RuntimeError("commit assets and reader before deployment")
    sha=git("rev-parse","HEAD")
    if git("ls-remote","origin","refs/heads/test/automated-edition-1").split()[0]!=sha:
        raise RuntimeError("review branch commit has not been pushed")
    receipt=json.loads((run/"production-receipt.json").read_text())
    require_current(run,receipt)
    if receipt.get("reader_hashes")!=reader_hashes(ROOT/receipt["reader"]): raise RuntimeError("reader changed after assembly")
    if receipt["defects"] or not receipt["reader"]: raise RuntimeError("production layers incomplete")
    key=os.environ.get("RENDER_API_KEY")
    if not key: raise RuntimeError("RENDER_API_KEY unavailable")
    service=api(f"/services/{SERVICE}",key)
    if service.get("branch")!="test/automated-edition-1": raise RuntimeError("review service is not bound to test branch")
    if service.get("repo", "").removesuffix(".git")!="https://github.com/oroknows-arch1/atlas-of-consequences": raise RuntimeError("review service uses another repository")
    task=api(f"/services/{SERVICE}/deploys",key,{"commitId":sha})
    deploy_id=task["id"]
    status=None
    for _ in range(50):
        data=api(f"/services/{SERVICE}/deploys/{deploy_id}",key)
        status=data.get("status")
        if status=="live":break
        if status in {"build_failed","update_failed","canceled","deactivated"}:break
        time.sleep(10)
    if status=="live" and data.get("commit",{}).get("id")!=sha: raise RuntimeError("deployed commit differs from requested commit")
    persisted=json.loads((run/"asset-persistence-receipt.json").read_text())
    require_current(run,persisted)
    asset_targets=[(asset["path"],asset["sha256"]) for asset in persisted.get("assets",[])]
    base_url=BASE+"/"+receipt["reader"].removeprefix("public/").removesuffix("index.html")
    integrated=False
    last_mismatch=None
    if status=="live":
        for _ in range(12):
            try:
                integrated=True
                for path,expected in asset_targets:
                    with urlopen(Request(BASE.rstrip("/") + path,headers={"Cache-Control":"no-cache"}),timeout=25) as response:
                        actual=hashlib.sha256(response.read()).hexdigest()
                    if actual!=expected:
                        integrated=False
                        last_mismatch=f"deployed bytes differ: {path}"
                        break
                if integrated: break
            except Exception as error:
                integrated=False
                last_mismatch=str(error)
            time.sleep(10)
    result={**binding(run),"reader_hashes":receipt["reader_hashes"],"branch":"test/automated-edition-1","commit":sha,
            "target":SERVICE,"deploy_id":deploy_id,"deployment_result":status,
            "base_url":BASE,"url":base_url,
            "asset_integration_status":"PASS" if integrated else "BLOCKED",
            "asset_integration_reason":None if integrated else last_mismatch,
            "status":"PASS" if status=="live" and integrated else "BLOCKED"}
    (run/"deployment-receipt.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2));return status!="live"
if __name__=="__main__":
    try:sys.exit(main(Path(sys.argv[1])))
    except Exception as e:print("DEPLOY BLOCKED:",e,file=sys.stderr);sys.exit(1)
