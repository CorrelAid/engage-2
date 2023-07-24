import uuid
from typing import Annotated, AsyncIterator

import pydantic
from api.auth.users import current_active_user
from database.session import async_session_maker
from fastapi import APIRouter, Depends, HTTPException, status
from models.project import Project
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class ReadProject(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    summary: str | None = None
    status: str


class CreateProject(pydantic.BaseModel):
    title: str
    summary: str | None = None
    status: str


class UpdateProject(pydantic.BaseModel):
    title: str | None = None
    summary: str | None = None
    status: str | None = None


async def get_project(project_id: uuid.UUID, session: AsyncSession) -> Project:
    try:
        project_entry = (
            await session.execute(select(Project).filter_by(id=project_id))
        ).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return project_entry


async def transactional_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker.begin() as session:
        yield session


SessionWithTransactionContext = Annotated[AsyncSession, Depends(transactional_session)]


@router.get(
    "/",
    response_description="List all projects",
    dependencies=[Depends(current_active_user)],
)
async def list_projects(
    session: SessionWithTransactionContext,
) -> list[ReadProject]:
    stmt = select(Project)
    projects = (await session.scalars(stmt)).all()
    return [
        ReadProject(id=p.id, title=p.title, summary=p.summary, status=p.status)
        for p in projects
    ]


@router.post(
    "/",
    response_description="Create a new project",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_active_user)],
)
async def create_project(
    project: CreateProject, session: SessionWithTransactionContext
) -> ReadProject:
    new_project = Project(id=uuid.uuid4(), **project.dict())
    session.add(new_project)
    return ReadProject(
        id=new_project.id,
        title=new_project.title,
        summary=new_project.summary,
        status=new_project.status,
    )


@router.get(
    "/{project_id}",
    response_description="Get a single project",
    dependencies=[Depends(current_active_user)],
)
async def read_project(
    project_id: uuid.UUID, session: SessionWithTransactionContext
) -> ReadProject:
    project_entry = await get_project(project_id, session)
    return ReadProject(
        id=project_entry.id,
        title=project_entry.title,
        summary=project_entry.summary,
        status=project_entry.status,
    )


@router.delete(
    "/{project_id}",
    response_description="Delete a single project",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: uuid.UUID, session: SessionWithTransactionContext
) -> None:
    project_entry = await get_project(project_id, session)
    await session.delete(project_entry)
    return None


@router.patch(
    "/{project_id}",
    response_description="Update a single project",
    dependencies=[Depends(current_active_user)],
)
async def update_project(
    project_id: uuid.UUID,
    project: UpdateProject,
    session: SessionWithTransactionContext,
) -> ReadProject:
    project_entry = await get_project(project_id, session)
    for key, value in project.model_dump(exclude_defaults=True).items():
        if getattr(project_entry, key) != value:
            setattr(project_entry, key, value)
    return ReadProject(
        id=project_entry.id,
        title=project_entry.title,
        summary=project_entry.summary,
        status=project_entry.status,
    )
