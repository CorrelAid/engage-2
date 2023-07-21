from typing import Annotated, Sequence
from uuid import UUID, uuid4

from database.session import get_async_session
from fastapi import APIRouter, Depends
from models.organization import Organization
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/organizations", tags=["organizations"])


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default=...)
    name: str = Field(default=...)


class OrganizationCreate(BaseModel):
    name: str = Field(default=...)


@router.post(path="", response_model=OrganizationRead)
def create_organization(
    organization: OrganizationCreate,
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Organization:
    new_organization = Organization(
        id=uuid4(),
        name=organization.name,
    )
    db_session.add(instance=new_organization)
    return new_organization


@router.get(path="", response_model=list[OrganizationRead])
async def list_organizations(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Sequence[Organization]:
    result = await db_session.execute(select(Organization))
    return result.scalars().all()
