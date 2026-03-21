from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate


class ExperimentRepository:


    async def create(
            self,
            db: AsyncSession,
            data: ExperimentCreate,
    ) -> Experiment:
        
        experiment = Experiment(**data.model_dump())

        db.add(experiment)

        await db.commit()
        await db.refresh(experiment)

        return experiment
    