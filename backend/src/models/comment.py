from datetime import datetime
from uuid import UUID

from models.base import Base
from sqlalchemy import DateTime, ForeignKey, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.NOW(),
    )
    created_by: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("user.id"),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.NOW(),
    )
    updated_by: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("user.id"),
        nullable=False,
    )
