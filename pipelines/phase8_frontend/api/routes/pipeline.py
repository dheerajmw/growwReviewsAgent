from fastapi import APIRouter

from ..services.artifacts import get_pipeline_status, get_publish_state

router = APIRouter(tags=["pipeline"])


@router.get("/pipeline/status")
def pipeline_status():
    return get_pipeline_status()


@router.get("/publish/state")
def publish_state():
    return get_publish_state()
