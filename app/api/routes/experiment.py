from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.experiment import ExperimentCreate, ExperimentRead, ExperimentUpdate
from app.services.experiment import ExperimentService
from app.core.exceptions import ExperimentNotFound
from app.api.dependencies.auth import get_current_user


router = APIRouter(prefix="/experiments", tags=["experiments"])

service = ExperimentService()


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=Sequence[ExperimentRead],
)
async def get_all_experiments(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    experiment_list = await service.read_all_experiments(db, current_user)
    return experiment_list


@router.get("/{experiment_number}",
            status_code=status.HTTP_200_OK,
            response_model=ExperimentRead,
)
async def get_one_experiment(
    experiment_number: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        experiment = await service.read_one_experiment(db, experiment_number, current_user)
        return experiment
    except ExperimentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=ExperimentRead,
)
async def create_experiment(
    data: ExperimentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    experiment = await service.create_experiment(db, data, current_user)

    return experiment
 
@router.patch(
     "/{experiment_number}",
     status_code=status.HTTP_200_OK,
     response_model=ExperimentRead,
 )
async def update_experiment(
    data: ExperimentUpdate,
    experiment_number: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        experiment = await service.update_experiment(db, data, experiment_number, current_user)
        return experiment
    except ExperimentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{experiment_number}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_experiment(
    experiment_number: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        await service.delete_experiment(db, experiment_number, current_user)
    except ExperimentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    