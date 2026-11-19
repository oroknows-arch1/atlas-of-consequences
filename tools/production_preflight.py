#!/usr/bin/env python3
"""Report every unavailable capability, without printing secret values."""
import os
import sys
from pathlib import Path
from production_state import binding, block, write

def main(run):
    missing = [name for name in ('OPENAI_API_KEY', 'RENDER_API_KEY') if not os.environ.get(name)]
    receipt = {**binding(run), 'status': 'BLOCKED' if missing else 'PASS',
               'missing_capabilities': missing, 'publication_authorized': False}
    write(run/'capability-receipt.json', receipt)
    # A new attempt always invalidates the previous final verdict.
    block(run, 'capability_preflight' if missing else 'production_orchestrator',
          'Missing: ' + ', '.join(missing) if missing else 'Production attempt in progress')
    print(receipt)
    return bool(missing)

if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
