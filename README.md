
# MEFI World Resonance

Live, anonymized resonance data powering Daily Field Reports and reproducible science.

## Quick Start
1. Create a new JSON under `data/YYYY/MM/ISO-TIMESTAMP.json` (UTC).
2. Ensure it matches `schemas/resonance-reading.schema.json`.
3. Push. CI validates, redacts, transforms, and updates `processed/`.
4. Docs site (GitHub Pages) updates automatically.

## Journal-Ready
- Daily CSVs under `processed/`
- Releasable monthly snapshots + DOI (via Zenodo) recommended.
