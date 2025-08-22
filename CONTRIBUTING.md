
# Contributing

## Add Data
- File path: `data/YYYY/MM/ISO-TIMESTAMP.json` (use UTC and replace `:` with `-`).
- Validate locally: `pip install jsonschema && jsonschema -i your.json schemas/resonance-reading.schema.json`.

## Decimal Shift
If you include `resonance_reading_hz_raw`, the pipeline computes `resonance_reading_hz = raw / 10`.

## Privacy
- Do not include names, emails, phone numbers, or exact addresses.
- Use `location_band.level` of `none`, `coarse-city`, or `coarse-region`.
- If city text is present, CI hashes it to `city_hash`.

Open a PR; CI will fail if anything violates schema/privacy.
