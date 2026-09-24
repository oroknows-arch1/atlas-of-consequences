# AOC-001 iPhone playback fix

Observed in Htmltest9.mp4: the canonical reader loaded, but the opening overlay was dismissed immediately before factual playback.

Fix:
- reduced-motion no longer skips the opening;
- story promo and soundtrack are lazy-loaded only when needed;
- story preload errors can no longer dismiss the factual opening;
- if unmuted story playback is blocked after the handoff, retry muted rather than ending the opening;
- factual media failure remains fail-open to the reader.

No new media generation or Runway spend.
