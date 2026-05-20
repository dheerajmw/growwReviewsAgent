# Deploy — React UI + Render BFF + Streamlit shell

| Component | Host | Role |
|-----------|------|------|
| **BFF** (FastAPI) | [Render](https://render.com) `groww-pulse-api` | `/api/v1/*` data API |
| **UI** (React Pulse 6) | Render `groww-pulse-ui` **or** local `npm run dev` | Same UI as localhost |
| **Streamlit Cloud** | [share.streamlit.io](https://share.streamlit.io) | Embeds React UI in iframe (not the old Python widgets) |

---

## Why Streamlit looked different from localhost

- **localhost:5173** = React app (`frontend/`) — Pulse 6 design  
- **Streamlit Cloud** (before) = Python `streamlit_app.py` only — different UI  

**Now:** Streamlit loads the **same React app** via `PULSE_UI_URL`.

---

## 1. Deploy on Render (blueprint)

`render.yaml` creates two services:

| Service | URL example |
|---------|-------------|
| `groww-pulse-api` | `https://groww-pulse-api.onrender.com` |
| `groww-pulse-ui` | `https://groww-pulse-ui.onrender.com` |

1. Render → **New Blueprint** → repo `growwReviewsAgent`, branch `main` → **Apply**
2. Wait for both services **Live**
3. Verify:
   ```bash
   curl https://groww-pulse-api.onrender.com/api/v1/health
   curl -I https://groww-pulse-ui.onrender.com
   ```

---

## 2. Streamlit Cloud secrets

**Settings → Secrets:**

```toml
PULSE_API_URL = "https://groww-pulse-api.onrender.com"
PULSE_UI_URL = "https://groww-pulse-ui.onrender.com"
```

Use your exact Render URLs. **Reboot** the app after saving.

You should see the React dashboard (Review Pulse header, glass nav, gradient bars) — same as local `npm run dev`.

---

## 3. Local development

**React UI (recommended):**

```bash
./scripts/serve_dashboard.sh
# or: cd frontend && npm run dev  →  http://localhost:5173
```

**Streamlit embed (like production):**

```bash
export PULSE_UI_URL=http://localhost:5173
cd frontend && npm run dev &
streamlit run streamlit_app.py
```

**Legacy Python Streamlit only:**

```bash
export PULSE_STREAMLIT_NATIVE=true
streamlit run streamlit_app.py
```

---

## 4. Build React for production manually

```bash
./scripts/build_react_deploy.sh
# Deploy frontend/dist via Render static site groww-pulse-ui
```

---

## Architecture

```text
Browser (Streamlit Cloud)
    └── iframe → groww-pulse-ui (React static)
            └── HTTPS → groww-pulse-api (FastAPI)
                    └── deploy/data artifacts
```
