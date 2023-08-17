from datetime import datetime
from uuid import UUID

from models.base import Base
from models.user import User
from sqlalchemy import JSON, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    legal_form: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )
    sectors: Mapped[list[str]] = mapped_column(postgresql.ARRAY(String(length=120)))
    contacts: Mapped[list[dict]] = mapped_column(
        JSON, nullable=False, server_default="[]"
    )
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
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        server_default=None,
    )
    archived_by: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("user.id"),
        nullable=True,
        server_default=None,
    )

    creator: Mapped[User] = relationship(
        "User", foreign_keys=[created_by], lazy="joined", uselist=False
    )
    updater: Mapped[User] = relationship(
        "User", foreign_keys=[updated_by], lazy="joined", uselist=False
    )
    archiver: Mapped[User] = relationship(
        "User", foreign_keys=[archived_by], lazy="joined", uselist=False
    )
