from fastapi import APIRouter

from app.schemas.experiment import Experiment
from app.db.data import experiment_list


router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.get("/")
async def get_all_experiments():
    return experiment_list
