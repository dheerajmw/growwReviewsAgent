# Render deploy bundle (`deploy/data/`)

The Phase 8 BFF reads `data/weekly/*`, `data/themes/*`, etc. Generated files are gitignored by default.

Before deploying the API to Render:

```bash
./scripts/prepare_render_data.sh
```

Then either:

1. **Commit** `deploy/data/` (add `!deploy/data/**` to `.gitignore` if you want it in git), and set on Render:
   ```bash
   PULSE_DATA_ROOT=/opt/render/project/src/deploy
   ```

2. **Persistent disk** on Render — run the weekly pipeline on the instance and keep `data/` on disk.

3. **CI sync** — extend GitHub Actions to upload artifacts to Render after each weekly run.

Streamlit does **not** need this folder; it only calls the Render API.
