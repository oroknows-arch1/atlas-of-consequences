# Atlas existing edition-factory integration retest — 2026-11-24

Owner instruction: execute production through the existing Atlas repository, not the discarded AOC-004 side implementation.

This file intentionally triggers `.github/workflows/atlas-edition-production.yml` through its established `content/AUTOMATED-TEST-001/**` path filter on the designated `test/automated-edition-1` branch.

**Scope:** re-run the existing `AET1-WC-002` validated-stage-input reader assembly and browser render gates, without model generation or publication. Workflow itself sets `ATLAS_READER_ONLY=1`, `ATLAS_ALLOW_COVERAGE_GENERATION=0` and permits only this test run directory.

**Strict limits:** no use or reuse of any previous AOC-004 content/assets, no Runway or paid media, no production deployment, no merge into main, and no claim of finished new edition. Preserve existing test receipts and report exact new CI results before starting a new content production attempt.

**Purpose:** establish whether the existing factory can genuinely run from the repo and reproduce an already approved/verified test edition. This is a foundation check, not a completed new edition.
