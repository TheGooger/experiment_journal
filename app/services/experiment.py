from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.experiment_repository import ExperimentRepository
from app.schemas.experiment import ExperimentCreate, ExperimentUpdate
from app.db.models.experiment import Experiment
from app.core.exceptions import ExperimentNotFound


class ExperimentService:

    def __init__(self):
        self.repository = ExperimentRepository()

    async def create_experiment(
            self,
            db: AsyncSession,
            data: ExperimentCreate,
    ) -> Experiment:
        experiment = await self.repository.create(db, data)

        return experiment
    

    async def read_all_experiments(
            self,
            db: AsyncSession,
    ) -> Sequence[Experiment]:
        
        experiment_list = await self.repository.read_all(db)

        return experiment_list
    

    async def read_one_experiment(
            self,
            db: AsyncSession,
            experiment_number: str,
    ) -> Optional[Experiment]:
        
        experiment = await self.repository.read_one(db, experiment_number)

        if experiment is None:
            raise ExperimentNotFound(f"Experiment with number {experiment_number} not found")
        
        return experiment
    

    async def update_experiment(
            self,
            db: AsyncSession,
            data: ExperimentUpdate,
            experiment_number: str,
    ) -> Optional[Experiment]:
        
        experiment = await self.repository.update(db, data, experiment_number)
        if experiment is None:
            raise ExperimentNotFound(f"Experiment with number {experiment_number} not found")
        return experiment
        
    