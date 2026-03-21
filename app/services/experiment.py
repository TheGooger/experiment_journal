from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.experiment_repository import ExperimentRepository
from app.schemas.experiment import ExperimentCreate
from app.db.models.experiment import Experiment


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
    