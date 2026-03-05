from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Experiment(BaseModel):
    id: str
    date: datetime
    is_done: bool
    project: Optional[str] = None
    goal: str
    object: str
    perovskite: Optional[str] = None
    samples: list[str]

    model_config = ConfigDict(from_attributes=True)
