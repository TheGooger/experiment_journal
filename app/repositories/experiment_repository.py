from typing import Optional, Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate, ExperimentUpdate


class ExperimentRepository:


    async def create(
            self,
            db: AsyncSession,
            data: ExperimentCreate,
            user_id: uuid.UUID,
    ) -> Experiment:
        
        experiment = Experiment(**data.model_dump())
        experiment.created_by_id = user_id

        db.add(experiment)

        await db.commit()
        await db.refresh(experiment)

        return experiment
    

    async def read_all(
            self,
            db:AsyncSession,
            user_id: uuid.UUID,
    ) -> Sequence[Experiment]:
        
        statement = select(Experiment).where(
            Experiment.created_by_id == user_id,
        ).order_by(Experiment.experiment_number)
        result = await db.execute(statement)

        return result.scalars().all()
    

    async def read_one(
            self,
            db: AsyncSession,
            experiment_number: str,
            user_id: uuid.UUID,
    ) -> Optional[Experiment]:
        
        statement = select(Experiment).where(Experiment.experiment_number == experiment_number)
        result = await db.execute(statement)
        experiment = result.scalar_one_or_none()


        if not experiment:
            return None
        

        if experiment.created_by_id != user_id:
            return None
        
        return experiment
    

    async def update(
            self,
            db: AsyncSession,
            data: ExperimentUpdate,
            experiment_number: str,
            user_id: uuid.UUID,
    ) -> Optional[Experiment]:
        
        statement = select(Experiment).where(Experiment.experiment_number == experiment_number)
        result = await db.execute(statement)
        experiment = result.scalar_one_or_none()


        if not experiment:
            return None
        

        if experiment.created_by_id != user_id:
            return None
        
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(experiment, key, value)
        
        await db.commit()
        await db.refresh(experiment)

        return experiment 


    async def delete(
            self, 
            db: AsyncSession,
            experiment_number: str,
            user_id: uuid.UUID,
    ) -> bool:
        

        statement = select(Experiment).where(Experiment.experiment_number == experiment_number)
        result = await db.execute(statement)
        experiment = result.scalar_one_or_none()

        if experiment is None:
            return False
        

        if experiment.created_by_id != user_id:
            return False
        
        await db.delete(experiment)
        await db.commit()
        return True
    