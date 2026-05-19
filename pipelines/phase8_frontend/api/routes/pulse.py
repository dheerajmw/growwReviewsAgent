from fastapi import APIRouter

from ..services.artifacts import get_pulse_latest, get_pulse_weeks

router = APIRouter(prefix="/pulse", tags=["pulse"])


@router.get("/latest")
def pulse_latest():
    return get_pulse_latest()


@router.get("/weeks")
def pulse_weeks():
    return {"weeks": get_pulse_weeks()}
