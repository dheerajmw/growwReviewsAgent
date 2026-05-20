# Deploy — React UI + Render BFF + Streamlit

| Component | Host | Role |
|-----------|------|------|
| **BFF** (FastAPI) | Render `groww-pulse-api` | `/api/v1/*` data API |
| **UI** (React Pulse 6) | Render `groww-pulse-ui` | Same as `npm run dev` → localhost:5173 |
| **Streamlit Cloud** | share.streamlit.io | **Embeds** the React UI full-screen |

---

## Streamlit Cloud (match localhost)

Streamlit loads the **same React app** as local `npm run dev` via iframe.

**Settings → Secrets:**

```toml
PULSE_API_URL = "https://groww-pulse-api.onrender.com"
PULSE_UI_URL = "https://groww-pulse-ui.onrender.com"
```

`PULSE_UI_URL` is optional on Streamlit Cloud (defaults to `groww-pulse-ui`). **Reboot** after changes.

**Dependencies:** Streamlit Cloud installs root `requirements.txt` only (streamlit, requests, pandas). Pipeline packages live in `requirements-pipeline.txt`.

Prerequisites:

1. Render blueprint applied — both `groww-pulse-api` and `groww-pulse-ui` **Live**
2. `curl https://groww-pulse-api.onrender.com/api/v1/health` → `{"status":"ok"}`
3. Open `https://groww-pulse-ui.onrender.com` — should show glass nav, sidebar, gradient background

Legacy Python-only UI: set `PULSE_STREAMLIT_NATIVE = true` in secrets.

---

## Local development

**Full stack (same as production UI):**

```bash
./scripts/serve_dashboard.sh
# React → http://localhost:5173
```

**Streamlit embed (like Streamlit Cloud):**

```bash
./scripts/run_streamlit_with_react.sh
```

Or manually:

```bash
export PULSE_API_URL=http://127.0.0.1:8080
export PULSE_UI_URL=http://localhost:5173
cd frontend && npm run dev &
streamlit run streamlit_app.py
```

---

## Render blueprint

See `render.yaml` for `groww-pulse-api` + `groww-pulse-ui`.

React build sets `VITE_API_BASE_URL` to the BFF URL. API CORS allows `groww-pulse-ui.onrender.com`.
