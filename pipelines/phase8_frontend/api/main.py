"""Phase 8 BFF — serve dashboard data from pipeline artifacts."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health, pipeline, pulse, themes

app = FastAPI(title="Groww Weekly Review Pulse API", version="1.0.0")

origins = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins + ["http://127.0.0.1:5173"],
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
