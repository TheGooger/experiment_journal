from datetime import datetime, timezone
import uuid

from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_number: Mapped[str] = mapped_column(String(10), nullable=False, unique=True, index=True)
    performed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    project: Mapped[str | None] = mapped_column(String(255))
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    experiment_subject: Mapped[str | None] = mapped_column(String(255))
    perovskite: Mapped[str | None] = mapped_column(String(255))
    samples: Mapped[list[str] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=True,
    )
