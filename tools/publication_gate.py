#!/usr/bin/env python3
"""Final receipt gate. The publication authority remains human."""
import hashlib, json, sys
from pathlib import Path
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads(p.read_text())
def main(run):
    candidate=read(run/"selected-edition-candidate.json")
    edition=candidate["candidate_id"]
    production=read(run/"production-receipt.json")
    assets=read(run/"asset-persistence-receipt.json")
    errors=list(production["defects"])
    required={x["scene_id"] for x in read(run/"visual_requirements.json")["output"]["requirements"] if x["required"]}
    integrated={x["scene_id"] for x in assets["assets"]}
    if required!=integrated: errors.append({"gate":"assets","reason":f"missing {sorted(required-integrated)}"})
    for item in assets["assets"]:
        path=ROOT/"public"/item["path"].lstrip('/')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item["sha256"]:
            errors.append({"gate":"persistence","reason":item["scene_id"]+" hash mismatch"})
    reader=ROOT/production["reader"] if production["reader"] else None
    if not reader or not reader.is_file(): errors.append({"gate":"reader","reason":"reader missing"})
    elif any(item["path"] not in reader.read_text() for item in assets["assets"]):
        errors.append({"gate":"integration","reason":"asset absent from reader"})
    for name in ("deployment-receipt", "rendered-qa", "visual-review", "benchmark-parity"):
        path=run/(name+".json")
        if not path.exists(): errors.append({"gate":name,"reason":"receipt missing"});continue
        data=read(path)
        if data.get("status")!="PASS": errors.append({"gate":name,"reason":"gate did not PASS"})
        if data.get("edition_id") and data["edition_id"]!=edition: errors.append({"gate":name,"reason":"wrong edition"})
    if not errors:
        deploy=read(run/"deployment-receipt.json")
        if deploy.get("branch")!="test/automated-edition-1" or not deploy.get("commit") or not deploy.get("url"):
            errors.append({"gate":"deployment","reason":"branch, commit or review URL missing"})
        else:
            for item in assets["assets"]:
                with urlopen(deploy["base_url"].rstrip('/')+item["path"],timeout=20) as res:
                    if hashlib.sha256(res.read()).hexdigest()!=item["sha256"]:
                        errors.append({"gate":"deployment","reason":item["scene_id"]+" deployed hash mismatch"})
    result={"edition_id":edition,"status":"BLOCKED" if errors else "PUBLICATION_CANDIDATE",
            "known_required_items":errors,"publication_authorized":False}
    (run/"publication-candidate-receipt.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2));return bool(errors)
if __name__=="__main__": sys.exit(main(Path(sys.argv[1])))
