from typing import Annotated, Literal, Sequence
from uuid import UUID, uuid4

from api.auth.users import current_active_user
from database.session import get_async_session
from fastapi import APIRouter, Depends
from models import Organization, OrganizationContact, OrganizationSector
from models.user import User
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/organizations", tags=["organizations"])

LEGAL_FORMS = Literal[
    "e.V. - Eingetragener Verein",
    "gGmbH - Gemeinnützige Gesellschaft mit beschränkter Haftung",
    "GmbH - Gesellschaft mit beschränkter Haftung",
    "gUG - Gemeinnützige Unternehmergesellschaft",
    "UG - Unternehmergesellschaft",
    "Stiftung",
]

SECTORS = Literal[
    "Bildung",
    "Gesundheit",
    "Kultur",
    "Sport",
    "Umwelt",
]


class OrganizationContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(default=...)
    role: str = Field(default=...)
    email: str = Field(default=...)
    phone: str = Field(default=...)


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default=...)
    name: str = Field(default=...)
    legal_form_name: LEGAL_FORMS = Field(default=...)
    sector_names: list[SECTORS] = Field(default=...)
    contacts: list[OrganizationContactRead] = Field(default=[])


class OrganizationCreate(BaseModel):
    name: str = Field(default=...)
    legal_form_name: LEGAL_FORMS = Field(default=...)
    sectors: list[SECTORS] = Field(default=...)
    contacts: list[OrganizationContactRead] = Field(default=[])


@router.post(path="", response_model=OrganizationRead)
async def create_organization(
    organization: OrganizationCreate,
    current_active_user: Annotated[User, Depends(current_active_user)],
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Organization:
    new_organization = Organization(
        id=uuid4(),
        name=organization.name,
        legal_form_name=organization.legal_form_name,
        created_by=current_active_user.id,
        updated_by=current_active_user.id,
        sectors=[
            OrganizationSector(sector_name=sector) for sector in organization.sectors
        ],
        contacts=[
            OrganizationContact(**contact.model_dump())
            for contact in organization.contacts
        ],
    )
    db_session.add(instance=new_organization)
    await db_session.commit()
    return new_organization


@router.get(path="", response_model=list[OrganizationRead])
async def list_organizations(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Sequence[Organization]:
    result = await db_session.execute(select(Organization))
    return result.scalars().all()
