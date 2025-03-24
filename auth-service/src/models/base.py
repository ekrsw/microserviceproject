
import datetime
from typing import Any

from sqlalchemy import event, DateTime, orm
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.sql import func
from typing import TypeVar
import uuid

from src.core.database import Base


T = TypeVar('T', bound='ModelBaseMixin')

class ModelBaseMixin(Base):
    __abstract__ = True
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
