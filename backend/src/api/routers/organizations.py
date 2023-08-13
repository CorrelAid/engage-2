from copy import copy
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID, uuid4

from api.auth.users import current_active_user
from database.session import transactional_session
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from models import Organization
from models.user import User
from pydantic import BaseModel, ConfigDict, EmailStr, TypeAdapter, model_validator
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

router = APIRouter(prefix="/organizations", tags=["organizations"])

LEGAL_FORM = Literal[
    "e.V. - Eingetragener Verein",
    "gGmbH - Gemeinnützige Gesellschaft mit beschränkter Haftung",
    "GmbH - Gesellschaft mit beschränkter Haftung",
    "gUG - Gemeinnützige Unternehmergesellschaft",
    "UG - Unternehmergesellschaft",
    "Stiftung",
]

SECTOR = Literal[
    "Bildung",
    "Gesundheit",
    "Kultur",
    "Sport",
    "Umwelt",
]

ORGANIZATION_CONTACT_ROLE = Literal[
    "Organization Contact",
    "Project Contact",
]


class OrganizationContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    role: ORGANIZATION_CONTACT_ROLE
    email: EmailStr
    phone: str


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    legal_form: LEGAL_FORM
    sectors: list[SECTOR]
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
    legal_form: LEGAL_FORM
    sectors: list[SECTOR]
    contacts: list[OrganizationContactRead] = []


class OrganizationContactUpdate(BaseModel):
    name: str
    role: ORGANIZATION_CONTACT_ROLE
    email: EmailStr
    phone: str


class OrganizationUpdate(BaseModel):
    name: str | None = None
    legal_form: LEGAL_FORM | None = None
    sectors: list[SECTOR] | None = None
    contacts: list[OrganizationContactRead] | None = None


class OrganizationStore:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(transactional_session)],
    ) -> None:
        self.session = session

    async def _get_orm_organization(self, organization_id: UUID) -> Organization:
        try:
            stmt = select(Organization).where(Organization.id == organization_id)
            organization_entry = (await self.session.execute(stmt)).scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return organization_entry

    async def get(self, organization_id: UUID) -> OrganizationRead:
        organization_entry = await self._get_orm_organization(organization_id)
        return TypeAdapter(OrganizationRead).validate_python(organization_entry)

    async def get_all(self) -> list[OrganizationRead]:
        organization_entries = (
            (await self.session.execute(select(Organization))).scalars().all()
        )
        return TypeAdapter(list[OrganizationRead]).validate_python(organization_entries)

    async def create(self, organization: OrganizationCreate, creator_id: UUID) -> UUID:
        new_organization = Organization(
            id=uuid4(),
            **organization.model_dump(exclude={"contacts"}),
            contacts=[contact.model_dump() for contact in organization.contacts],
            created_by=creator_id,
            updated_by=creator_id,
        )
        self.session.add(new_organization)
        return new_organization.id

    async def delete(self, organization_id: UUID) -> None:
        organization_entry = await self._get_orm_organization(organization_id)
        await self.session.delete(organization_entry)
        return None

    async def update(
        self,
        organization_id: UUID,
        organization: OrganizationUpdate,
        updater_id: UUID,
    ) -> OrganizationRead:
        organization_entry = await self._get_orm_organization(organization_id)
        for key, value in organization.model_dump(exclude_defaults=True).items():
            if getattr(organization_entry, key) != value:
                setattr(organization_entry, key, value)
        organization_entry.updated_by = updater_id
        organization_entry.updated_at = datetime.utcnow()
        return TypeAdapter(OrganizationRead).validate_python(organization_entry)

    async def archive(
        self, organization_id: UUID, archiver_id: UUID
    ) -> OrganizationRead:
        organization_entry = await self._get_orm_organization(organization_id)
        organization_entry.archived_by = archiver_id
        organization_entry.archived_at = datetime.utcnow()
        return TypeAdapter(OrganizationRead).validate_python(organization_entry)

    async def unarchive(self, organization_id: UUID) -> OrganizationRead:
        organization_entry = await self._get_orm_organization(organization_id)
        organization_entry.archived_by = None
        organization_entry.archived_at = None
        return TypeAdapter(OrganizationRead).validate_python(organization_entry)


@router.get(
    path="/",
    response_description="List of organizations",
    dependencies=[Depends(current_active_user)],
)
async def list_organizations(
    project_store: Annotated[OrganizationStore, Depends()],
) -> list[OrganizationRead]:
    return await project_store.get_all()


@router.post(
    path="/",
    response_description="Create a new organization",
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    organization: Annotated[OrganizationCreate, Body(...)],
    project_store: Annotated[OrganizationStore, Depends()],
    creator: User = Depends(current_active_user),
) -> OrganizationRead:
    organization_id = await project_store.create(
        organization=organization, creator_id=creator.id
    )
    return await project_store.get(organization_id=organization_id)


@router.get(
    path="/{organization_id}",
    response_description="Get a single organization",
    dependencies=[Depends(current_active_user)],
)
async def get_organization(
    organization_id: Annotated[UUID, Path(...)],
    project_store: Annotated[OrganizationStore, Depends()],
) -> OrganizationRead:
    return await project_store.get(organization_id)


@router.delete(
    path="/{organization_id}",
    response_description="Delete a single organization",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_organization(
    organization_id: Annotated[UUID, Path(...)],
    project_store: Annotated[OrganizationStore, Depends()],
) -> None:
    return await project_store.delete(organization_id)


@router.patch(
    path="/{organization_id}",
    response_description="Update a single organization",
)
async def update_organization(
    organization_id: Annotated[UUID, Path(...)],
    organization: Annotated[OrganizationUpdate, Body(...)],
    project_store: Annotated[OrganizationStore, Depends()],
    updater: User = Depends(current_active_user),
) -> OrganizationRead:
    await project_store.update(organization_id, organization, updater_id=updater.id)
    return await project_store.get(organization_id)


@router.patch(
    path="/{organization_id}/archive",
    response_description="Archive a single organization",
)
async def archive_organization(
    organization_id: Annotated[UUID, Path(...)],
    project_store: Annotated[OrganizationStore, Depends()],
    archiver: User = Depends(current_active_user),
) -> OrganizationRead:
    await project_store.archive(organization_id, archiver_id=archiver.id)
    return await project_store.get(organization_id)


@router.patch(
    path="/{organization_id}/unarchive",
    response_description="Unarchive a single organization",
)
async def unarchive_organization(
    organization_id: Annotated[UUID, Path(...)],
    project_store: Annotated[OrganizationStore, Depends()],
) -> OrganizationRead:
    await project_store.unarchive(organization_id)
    return await project_store.get(organization_id)
