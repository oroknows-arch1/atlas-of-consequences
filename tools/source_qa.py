#!/usr/bin/env python3
"""Verify inspectable source URLs with explicit, provenance-preserving fallbacks."""
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from production_state import binding, read, write

def candidate_urls(source):
    """Return the declared source first, then only its explicit canonical fallbacks."""
    return [source["url"], *source.get("fallback_urls", [])]

def resolve_source(source, opener=urlopen):
    attempts = []
    result = {"source_id": source["id"], "url": source["url"], "status": "BLOCKED"}
    for index, url in enumerate(candidate_urls(source)):
        for attempt in range(1, 4):
            try:
                request = Request(url, headers={"User-Agent": "AtlasSourceVerifier/1.0"})
                with opener(request, timeout=25) as response:
                    if response.status != 200 or not response.read(2048):
                        raise ValueError("empty or unavailable source")
                    attempts.append({"url": url, "attempt": attempt, "status": "PASS"})
                    result.update(status="PASS", resolved_url=response.url, fallback_used=index > 0, attempts=attempts)
                return result
            except Exception as error:
                attempts.append({"url": url, "attempt": attempt, "status": "BLOCKED", "reason": str(error)})
    result["attempts"] = attempts
    result["reason"] = attempts[-1]["reason"] if attempts else "no source URL declared"
    return result

def sources(run):
    items = read(run / "source-register.json")
    override_path = run / "source-access-overrides.json"
    if override_path.exists():
        overrides = read(override_path)
        for item in items:
            item.update(overrides.get(item["id"], {}))
    return items

def main(run):
    checks = [resolve_source(source) for source in sources(run)]
    receipt = {**binding(run), "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "BLOCKED", "sources": checks}
    write(run / "source-qa.json", receipt)
    print(json.dumps(receipt, indent=2))
    return receipt["status"] != "PASS"

if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
