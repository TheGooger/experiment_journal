from typing import Optional

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
        
    