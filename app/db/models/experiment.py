from datetime import datetime, timezone

from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy import false, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class Experiments(Base):
    __tablename__ = "experiments"

    
