
# Methods & Data Handling

## Schema
All readings must conform to `schemas/resonance-reading.schema.json`.

## Decimal Shift Rule
If `resonance_reading_hz_raw` is present, pipeline creates `resonance_reading_hz = raw / 10`.

## Privacy Defaults
- No PII. Pseudonymous `node_id` only.
- Location is by coarse band; cities (if supplied) are hashed by CI.
- CI fails on schema or privacy violations.

## Processing
Validated JSON is copied to `processed/` and a daily CSV is generated.
