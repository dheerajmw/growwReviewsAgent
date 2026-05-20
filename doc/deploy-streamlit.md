# Deploy — React UI + Render BFF + Streamlit

| Component | Host | Role |
|-----------|------|------|
| **BFF** (FastAPI) | [Render](https://render.com) `groww-pulse-api` | `/api/v1/*` data API |
| **UI** (React Pulse 6) | Render `groww-pulse-ui` **or** local `npm run dev` | Full Stitch UI |
| **Streamlit Cloud** | [share.streamlit.io](https://share.streamlit.io) | **Native** Pulse-styled dashboard (recommended) |

---

## Streamlit Cloud (recommended setup)

Streamlit runs the **Python Pulse 6 UI** (`streamlit_lib/ui.py` + `components.py`) — not an iframe. This avoids broken CSS / blue placeholder blocks.

**Settings → Secrets:**

```toml
PULSE_API_URL = "https://groww-pulse-api.onrender.com"
```

Do **not** set `PULSE_UI_URL` unless you explicitly want the React iframe embed.

**Reboot** the app after saving secrets.

You should see: sidebar navigation, green top bar, metric cards, theme bars, and doc/draft cards.

Optional: open the full React app via **Open full React dashboard ↗** or `https://groww-pulse-ui.onrender.com`.

---

## Optional: embed React in Streamlit (advanced)

Only if you need the exact Vite build inside Streamlit:

```toml
PULSE_API_URL = "https://groww-pulse-api.onrender.com"
PULSE_USE_REACT_UI = true
PULSE_UI_URL = "https://groww-pulse-ui.onrender.com"
```

Requires `groww-pulse-ui` deployed and healthy. Redeploy UI after changing `vite` `base` to `/`.

---

## 1. Deploy on Render (blueprint)

`render.yaml` creates:

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

## 2. Local development

**React UI (recommended):**

```bash
./scripts/serve_dashboard.sh
# or: cd frontend && npm run dev  →  http://localhost:5173
```

**Streamlit (native Pulse UI):**

```bash
export PULSE_API_URL=http://127.0.0.1:8080
streamlit run streamlit_app.py
```

**Streamlit + React iframe (like optional production):**

```bash
export PULSE_API_URL=http://127.0.0.1:8080
export PULSE_USE_REACT_UI=true
export PULSE_UI_URL=http://localhost:5173
cd frontend && npm run dev &
streamlit run streamlit_app.py
```

---

## 3. Build React for production manually

```bash
./scripts/build_react_deploy.sh
```

`VITE_API_BASE_URL` must point at your Render BFF when building for `groww-pulse-ui`.
