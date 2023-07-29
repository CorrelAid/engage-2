from datetime import datetime
from uuid import UUID

from models.base import Base
from models.user import User
from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrganizationContact(Base):
    __tablename__ = "organization_contacts"

    organization_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("organizations.id"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(length=255), primary_key=True)
    role: Mapped[str] = mapped_column(String(length=255), nullable=False)
    email: Mapped[str] = mapped_column(String(length=255), nullable=False)
    phone: Mapped[str] = mapped_column(String(length=255), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="contacts"
    )


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    legal_form: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )
    sectors: Mapped[list[str]] = mapped_column(postgresql.ARRAY(String(length=120)))
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

    contacts: Mapped[list["OrganizationContact"]] = relationship(
        "OrganizationContact",
        lazy="selectin",
        cascade="all,delete",
        back_populates="organization",
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

    def toggle_archive(self, archived_by: UUID) -> None:
        if self.archived_at is None:
            self.archived_at = datetime.utcnow()
            self.archived_by = archived_by
        else:
            self.archived_at = None
            self.archived_by = None
