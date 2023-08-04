from copy import copy
from datetime import datetime
from typing import Annotated, Any, Literal, Sequence
from uuid import UUID, uuid4

from api.auth.users import current_active_user
from database.session import get_async_session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Organization, OrganizationContact
from models.user import User
from pydantic import BaseModel, ConfigDict, model_validator
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

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


async def get_organization_by_id(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    organization_id: Annotated[UUID, Path()],
) -> Organization:
    organization = await db_session.get(Organization, organization_id)
    if organization is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Organization not found.")
    return organization


class OrganizationContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    role: str
    email: str
    phone: str


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    legal_form: LEGAL_FORMS
    sectors: list[SECTORS]
    contacts: list[OrganizationContactRead]
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    archived_at: datetime | None = None
    archived_by: str | None = None

    @model_validator(mode="before")
    @classmethod
    def set_user_names(cls, data: Any) -> Any:
        data = copy(x=data)
        data.created_by = data.creator.name
        data.updated_by = data.updater.name
        data.archived_by = data.archiver.name if data.archiver else None
        return data


class OrganizationCreate(BaseModel):
    name: str
    legal_form: LEGAL_FORMS
    sectors: list[SECTORS]
    contacts: list[OrganizationContactRead] = []


@router.post(path="", response_model=OrganizationRead)
async def create_organization(
    organization: OrganizationCreate,
    current_active_user: Annotated[User, Depends(current_active_user)],
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Organization:
    new_organization = Organization(
        id=uuid4(),
        name=organization.name,
        legal_form=organization.legal_form,
        created_by=current_active_user.id,
        updated_by=current_active_user.id,
        sectors=organization.sectors,
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


@router.get(path="/{organization_id}", response_model=OrganizationRead)
async def get_organization(
    organization: Annotated[Organization, Depends(get_organization_by_id)],
) -> Organization:
    return organization


class OrganizationUpdate(BaseModel):
    name: str
    legal_form: LEGAL_FORMS
    sectors: list[SECTORS]
    contacts: list[OrganizationContactRead] = []


@router.patch(path="/{organization_id}", response_model=OrganizationRead)
async def update_organization(
    organization: Annotated[Organization, Depends(get_organization_by_id)],
    updated_organization: OrganizationUpdate,
    current_active_user: Annotated[User, Depends(current_active_user)],
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Organization:
    for key, value in updated_organization.model_dump(
        exclude_defaults=True, exclude={"contacts": True}
    ).items():
        if getattr(organization, key) != value:
            setattr(organization, key, value)
    organization.updated_by = current_active_user.id
    delete_query = delete(table=OrganizationContact).where(
        OrganizationContact.organization_id == organization.id
    )
    await db_session.execute(statement=delete_query)
    if updated_organization.contacts:
        insert_query = insert(table=OrganizationContact)
        await db_session.execute(
            statement=insert_query,
            params=[
                {"organization_id": organization.id, **contact.model_dump()}
                for contact in updated_organization.contacts
            ],
        )
    return organization


@router.patch(path="/{organization_id}/archive", response_model=OrganizationRead)
async def archive_organization(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    organization: Annotated[Organization, Depends(get_organization_by_id)],
    current_active_user: Annotated[User, Depends(current_active_user)],
) -> Organization:
    organization.toggle_archive(archived_by=current_active_user.id)
    await db_session.commit()
    await db_session.refresh(organization)
    return organization


@router.delete(path="/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    organization: Annotated[Organization, Depends(get_organization_by_id)],
) -> None:
    await db_session.delete(organization)
