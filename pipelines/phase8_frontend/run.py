#!/usr/bin/env python3
"""Run Phase 8 BFF API."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "pipelines.phase8_frontend.api.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
