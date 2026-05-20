# Render deploy troubleshooting (groww-pulse-api)

## Blueprint says “Failed deployment”

1. Open the Blueprint in [Render Dashboard](https://dashboard.render.com) → click the **failed** service **`groww-pulse-api`**.
2. Open **Logs** (not only the Blueprint summary). The last lines tell you which fix below applies.
3. Confirm repo: **`dheerajmw/growwReviewsAgent`**, branch **`main`**, **Root Directory** = *(empty)*.
4. If a previous Blueprint left a broken service, delete the Blueprint group or suspend the old `groww-pulse-api`, then **New + → Blueprint** again.
5. After fixing `render.yaml` on GitHub, use **Manual Deploy → Deploy latest commit** (or re-apply Blueprint).

**Quick health check after Live:**

```bash
curl -sS https://YOUR-SERVICE.onrender.com/api/v1/health
# {"status":"ok"}
```

If you see **“Service Suspended”** (HTML 503), open the service → **Resume** (not a build failure).

---

## Check the failure type

In Render → your service → **Events** or **Logs**:

| Log section | Meaning |
|-------------|---------|
| **Build failed** | `pip install` or missing `requirements-bff.txt` |
| **Deploy failed** | App crash on start (import error, wrong command) |
| **Health check failed** | App runs but `/api/v1/health` not reachable in time |

**Typical log lines:**

| Log snippet | Fix |
|-------------|-----|
| `ModuleNotFoundError: No module named 'pipelines'` | Root Directory must be empty; repo must be `growwReviewsAgent` |
| `uvicorn: command not found` | Use start command `python -m uvicorn ...` (see `render.yaml` on `main`) |
| `No open ports` / `Address already in use` | Start must use `--port $PORT` |
| `Health check failed` | Wait for free-tier cold start; redeploy; confirm path `/api/v1/health` |
| `Service Suspended` | Resume service in dashboard (billing or manual suspend) |

Copy the **last 20 lines** of the failed log when asking for help.

---

## Fix 1 — Blueprint / YAML

Use the simplified `render.yaml` on `main` (no optional `FRONTEND_ORIGIN` block that can break sync).

1. Pull latest `main` from GitHub.
2. Delete the failed Blueprint group (if stuck), or create a **new** Blueprint.
3. **New +** → **Blueprint** → repo **`dheerajmw/growwReviewsAgent`** → branch **`main`** → **Apply**.

**Root Directory** must be **empty** (repo root contains `render.yaml`).

---

## Fix 2 — Manual Web Service (if Blueprint keeps failing)

1. **New +** → **Web Service** (not Blueprint).
2. Repository: `dheerajmw/growwReviewsAgent`, branch `main`.
3. Settings:

| Field | Value |
|--------|--------|
| Name | `groww-pulse-api` |
| Root Directory | *(leave blank)* |
| Runtime | Python 3 |
| Build Command | `pip install --upgrade pip && pip install -r requirements-bff.txt` |
| Start Command | `python -m uvicorn pipelines.phase8_frontend.api.main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/api/v1/health` |

4. Environment:

| Key | Value |
|-----|--------|
| `PYTHON_VERSION` | `3.11.9` |
| `PULSE_DATA_ROOT` | `/opt/render/project/src/deploy` |

5. **Create Web Service**.

---

## Fix 3 — Wrong GitHub repo / folder

- Repo must be **`growwReviewsAgent`**, not a parent folder without `render.yaml`.
- Do **not** point Root Directory at `Milestone3` unless the repo root is above this project.

---

## Fix 4 — Verify after Live

```bash
curl https://YOUR-SERVICE.onrender.com/api/v1/health
```

Expect: `{"status":"ok"}`

---

## Fix 5 — Empty dashboard data

Health OK but no pulse data → ensure `deploy/data/` is on `main`:

```bash
./scripts/prepare_render_data.sh
git add deploy/data && git commit -m "Update deploy data" && git push
```

Then Render → **Manual Deploy** → **Deploy latest commit**.
