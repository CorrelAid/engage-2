from uuid import UUID

from models.base import Base
from sqlalchemy import String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class Project(Base):
    __tablename__ = "project"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(length=20), nullable=False)
