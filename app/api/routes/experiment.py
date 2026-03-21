from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.experiment import ExperimentCreate, ExperimentRead
from app.services.experiment import ExperimentService


router = APIRouter(prefix="/experiments", tags=["experiments"])

service = ExperimentService()


# @router.get("/")
# async def get_all_experiments() -> list[ExperimentRead]:
#     return experiment_list


@router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=ExperimentRead,
)
async def create_experiment(
    data: ExperimentCreate,
    db: AsyncSession = Depends(get_db),
):
    experiment = await service.create_experiment(db, data)

    return experiment
 