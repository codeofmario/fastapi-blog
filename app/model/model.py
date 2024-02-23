from datetime import datetime
from uuid import uuid4

from sqlalchemy import func, types
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Model(DeclarativeBase):
    id: Mapped[str] = mapped_column(types.Uuid, primary_key=True, default=uuid4, index=True)

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now(), nullable=False)
