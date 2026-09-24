# AOC-001 Live Opening Bugfix — 2026-09-24

Observed from iPhone screen recording `Htmltest9.mp4`:

- canonical reader loaded successfully;
- hybrid opening did not take over the viewport;
- reader was revealed immediately;
- no WHAT'S REAL playback, STORY / FICTION crossing, story promo, or Tap for sound experience was observed.

## Root causes fixed

1. `prefers-reduced-motion: reduce` must not bypass the explicitly approved opening. It may disable fades/transitions only.
2. The story promo must not preload in a way that can fail before the factual film has played. Its source is loaded only when the factual branch ends.
3. A story-media error may fail open only after the factual branch has completed; it must never dismiss the opening before factual playback begins.
4. The factual film remains the authoritative first media event. If it fails, reveal the reader rather than trapping the user.

No new media generation is required and no Runway credits are spent by this fix.
