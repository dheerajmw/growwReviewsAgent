# Deploy — Streamlit UI + Render BFF

| Component | Host | Role |
|-----------|------|------|
| **BFF** (FastAPI) | [Render](https://render.com) | Serves `data/` artifacts via `/api/v1/*` |
| **UI** | [Streamlit Cloud](https://share.streamlit.io) | Dashboard; calls BFF over HTTPS |
| **MCP** (Docs/Gmail) | Render (separate repo) | Unchanged — `MCP_SERVER_URL` |

The React/Vite app in `frontend/` remains optional for local dev.

---

## 1. Deploy BFF on Render

1. Connect [growwReviewsAgent](https://github.com/dheerajmw/growwReviewsAgent) to Render.
2. Use the blueprint `render.yaml` or create a **Web Service**:
   - **Build:** `pip install -r requirements-bff.txt`
   - **Start:** `python -m uvicorn pipelines.phase8_frontend.api.main:app --host 0.0.0.0 --port $PORT`
   - **Health check:** `/api/v1/health`
3. Prepare data (see [deploy/README.md](../deploy/README.md)):
   ```bash
   ./scripts/prepare_render_data.sh
   ```
   Set env `PULSE_DATA_ROOT` to your bundle path if not using repo-root `data/`.
4. Environment variables on Render:

   | Variable | Example |
   |----------|---------|
   | `FRONTEND_ORIGIN` | `https://your-app.streamlit.app` |
   | `PULSE_DATA_ROOT` | `/opt/render/project/src/deploy` (optional) |

5. Note the service URL, e.g. `https://groww-pulse-api.onrender.com`.

CORS allows `https://*.streamlit.app` automatically.

---

## 2. Deploy UI on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
2. Repository: `dheerajmw/growwReviewsAgent`, branch `main`.
3. **Main file path:** `streamlit_app.py`
4. **Requirements file:** `requirements-streamlit.txt`
5. **Secrets** (TOML):

   ```toml
   PULSE_API_URL = "https://groww-pulse-api.onrender.com"
   ```

6. Deploy. Pages live under `pages/` (Weekly Pulse, Themes, Pipeline, Settings).

---

## 3. Local Streamlit (against local or Render API)

```bash
pip install -r requirements-streamlit.txt
export PULSE_API_URL=http://127.0.0.1:8080   # or your Render URL
streamlit run streamlit_app.py
```

Open http://localhost:8501

---

## 4. Verify

```bash
curl https://YOUR-RENDER-SERVICE.onrender.com/api/v1/health
# {"status":"ok"}

curl https://YOUR-RENDER-SERVICE.onrender.com/api/v1/pulse/latest
```

In Streamlit → **Settings** → **Save & test** should show `Connected: {'status': 'ok'}`.

---

## Architecture

```text
Streamlit Cloud  --HTTPS GET-->  Render (groww-pulse-api)
                                      |
                                      reads data/weekly, data/themes
GitHub Actions (weekly)  -->  generates data/  -->  sync to Render disk or deploy/
```
