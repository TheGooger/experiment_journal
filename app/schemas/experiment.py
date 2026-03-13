from datetime import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ExperimentBase(BaseModel):
    experiment_number: str = Field(max_length=10)
    performed_at: datetime
    is_completed: bool
    project: Optional[str] = None
    goal: str
    experiment_subject: Optional[str] = None
    perovskite: Optional[str] = None
    samples: Optional[list[str]] = None


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentUpdate(BaseModel):
    experiment_number: Optional[str] = None
    performed_at: Optional[datetime] = None
    is_completed: Optional[bool] = None
    project: Optional[str] = None
    goal: Optional[str] = None
    experiment_subject: Optional[str] = None
    perovskite: Optional[str] = None
    samples: Optional[list[str]] = None


class ExperimentRead(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
