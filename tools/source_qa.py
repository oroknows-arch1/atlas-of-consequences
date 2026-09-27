#!/usr/bin/env python3
"""Verify inspectable source URLs. Never invent a replacement source to clear a gate."""
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from production_state import binding, read, write

def main(run):
    checks=[]
    for source in read(run/'source-register.json'):
        result={'source_id':source['id'], 'url':source['url'], 'status':'BLOCKED'}
        for attempt in range(1,4):
            try:
                request=Request(source['url'],headers={'User-Agent':'AtlasSourceVerifier/1.0'})
                with urlopen(request,timeout=25) as response:
                    if response.status!=200 or not response.read(2048): raise ValueError('empty or unavailable source')
                    result.update(status='PASS', resolved_url=response.url)
                break
            except Exception as error:
                result['reason']=str(error)
        checks.append(result)
    receipt={**binding(run),'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'BLOCKED','sources':checks}
    write(run/'source-qa.json',receipt)
    print(json.dumps(receipt,indent=2))
    return receipt['status']!='PASS'

if __name__=='__main__':sys.exit(main(Path(sys.argv[1])))
