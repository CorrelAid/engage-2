from datetime import datetime
from uuid import UUID

from models.base import Base
from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LegalForm(Base):
    __tablename__ = "legal_forms"

    name: Mapped[str] = mapped_column(String(length=255), primary_key=True)


class Sector(Base):
    __tablename__ = "sectors"

    name: Mapped[str] = mapped_column(String(length=255), primary_key=True)


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
        back_populates="contacts",
    )


class OrganizationSector(Base):
    __tablename__ = "organization_sectors"

    organization_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("organizations.id"),
        primary_key=True,
    )
    sector_name: Mapped[str] = mapped_column(
        String(length=255),
        ForeignKey("sectors.name"),
        primary_key=True,
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="sectors",
    )


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    legal_form_name: Mapped[str] = mapped_column(
        String(length=255),
        ForeignKey("legal_forms.name"),
        nullable=False,
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

    contacts: Mapped[list["OrganizationContact"]] = relationship(
        back_populates="organization",
        lazy="selectin",
    )
    sectors: Mapped[list["OrganizationSector"]] = relationship(
        back_populates="organization",
        lazy="selectin",
    )

    @property
    def sector_names(self) -> list[str]:
        return [sector.sector_name for sector in self.sectors]
