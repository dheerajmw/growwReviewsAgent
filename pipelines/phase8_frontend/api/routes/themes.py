from fastapi import APIRouter

from ..services.artifacts import get_clusters_summary, get_ranked

router = APIRouter(prefix="/themes", tags=["themes"])


@router.get("/ranked")
def themes_ranked():
    return get_ranked()


@router.get("/clusters")
def themes_clusters():
    return get_clusters_summary()
