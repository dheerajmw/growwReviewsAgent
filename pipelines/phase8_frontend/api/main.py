"""Phase 8 BFF — serve dashboard data from pipeline artifacts."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health, pipeline, pulse, themes

app = FastAPI(title="Groww Weekly Review Pulse API", version="1.0.0")

_default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "https://groww-pulse-ui.onrender.com",
]
_extra = [o.strip() for o in os.environ.get("FRONTEND_ORIGIN", "").split(",") if o.strip()]
origins = list(dict.fromkeys(_default_origins + _extra))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://(.*\.streamlit\.app|.*\.onrender\.com)",
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(pulse.router, prefix="/api/v1")
app.include_router(themes.router, prefix="/api/v1")
app.include_router(pipeline.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"service": "groww-review-pulse-api", "docs": "/docs"}
