#!/usr/bin/env python3
"""Coverage gate: no benchmark operation may disappear behind a conceptual node."""
import ast
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={'world_change','evidence','geography','perspectives','routes','story','visual_intent',
          'editorial_assembly','visual_generation','visual_qa','binary_persistence','hash_provenance',
          'repository_integration','reader_assembly','source_register','deployment','rendered_inspection',
          'repair','redeployment','final_qa','publication_review'}

def validate(contract):
 errors=[]
 operations=contract['operations']
 ids=[op['operation'] for op in operations]
 if set(ids)!=REQUIRED or len(ids)!=len(set(ids)):errors.append('manufacturing trace has missing, extra or duplicate operations')
 for op in operations:
  if op.get('kind') not in {'automated_worker','automated_gate','human_authority_gate'}:errors.append('invalid coverage kind')
  if op.get('kind')=='human_authority_gate':
   if op['operation']!='publication_review':errors.append('routine production became a human gate')
   continue
  if not op.get('owner') or not op.get('receipt') or not op.get('repair_owner'):errors.append('unowned or unverifiable operation: '+op['operation'])
  entry=op.get('entrypoint','').split(':')
  path=ROOT/entry[0]
  if not path.is_file():errors.append('missing executable '+entry[0]);continue
  if path.suffix=='.py':
   names={n.name for n in ast.walk(ast.parse(path.read_text())) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
   if len(entry)!=2 or entry[1] not in names:errors.append('missing executable function '+op.get('entrypoint',''))
 return errors

if __name__=='__main__':
 errors=validate(json.loads((ROOT/'atlas/contracts/manufacturing-trace.json').read_text()))
 print('MANUFACTURING TRACE COVERAGE: '+('BLOCKED' if errors else 'PASS'))
 for e in errors:print(e)
 sys.exit(bool(errors))
