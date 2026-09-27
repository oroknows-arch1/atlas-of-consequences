#!/usr/bin/env python3
"""Deploy -> inspect -> repair -> redeploy, bounded to three attempts."""
import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args):return subprocess.run(args,cwd=ROOT).returncode
def main(directory):
    run_dir=Path(directory)
    for attempt in range(1,4):
        if run(sys.executable,"tools/deploy_review.py",str(run_dir)):return 1
        receipt=json.loads((run_dir/"deployment-receipt.json").read_text())
        result=run("node","tools/rendered_qa.cjs",receipt["url"],str(run_dir/"rendered-qa.json"),str(run_dir/"screenshots"))
        if not (run_dir/"rendered-qa.json").exists():return 1
        vision=run(sys.executable,"tools/review_rendered.py",str(run_dir))
        if not result and not vision:return 0
        if attempt==3:return 1
        if run(sys.executable,"tools/repair_reader.py",str(run_dir)):return 1
        css=ROOT/"public"/"review"/receipt["edition_id"].lower()/"reader.css"
        if run("git","add",str(css.relative_to(ROOT))) or run("git","commit","-m",f"Repair rendered Atlas reader attempt {attempt}") or run("git","push","origin","HEAD:test/automated-edition-1"):
            return 1
    return 1
if __name__=="__main__":sys.exit(main(sys.argv[1]))
