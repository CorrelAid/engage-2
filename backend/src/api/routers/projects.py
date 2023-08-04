import uuid
from typing import Annotated

from api.auth.users import current_active_user
from database.session import transactional_session
from fastapi import APIRouter, Depends, HTTPException, status
from models.project import Project
from pydantic import BaseModel, ConfigDict, TypeAdapter
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class ReadProject(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    summary: str | None = None
    status: str


class CreateProject(BaseModel):
    title: str
    summary: str | None = None
    status: str


class UpdateProject(BaseModel):
    title: str | None = None
    summary: str | None = None
    status: str | None = None


class ProjectStore:
    def __init__(
        self, session: Annotated[AsyncSession, Depends(transactional_session)]
    ):
        self.session = session

    async def _get_orm_project(self, project_id: uuid.UUID) -> Project:
        try:
            project_entry = (
                await self.session.execute(select(Project).filter_by(id=project_id))
            ).scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return project_entry

    async def get(self, project_id: uuid.UUID) -> ReadProject:
        project_entry = await self._get_orm_project(project_id)
        return TypeAdapter(ReadProject).validate_python(project_entry)

    async def get_all(self) -> list[ReadProject]:
        stmt = select(Project)
        projects = (await self.session.scalars(stmt)).all()
        return TypeAdapter(list[ReadProject]).validate_python(projects)

    async def create(self, project: CreateProject) -> ReadProject:
        new_project = Project(id=uuid.uuid4(), **project.model_dump())
        self.session.add(new_project)
        return TypeAdapter(ReadProject).validate_python(new_project)

    async def delete(self, project_id: uuid.UUID) -> None:
        project_entry = await self._get_orm_project(project_id)
        await self.session.delete(project_entry)
        return None

    async def update(
        self, project_id: uuid.UUID, project: UpdateProject
    ) -> ReadProject:
        project_entry = await self._get_orm_project(project_id)
        for key, value in project.model_dump(exclude_defaults=True).items():
            if getattr(project_entry, key) != value:
                setattr(project_entry, key, value)
        return TypeAdapter(ReadProject).validate_python(project_entry)


@router.get(
    "/",
    response_description="List all projects",
    dependencies=[Depends(current_active_user)],
)
async def list_projects(
    project_store: Annotated[ProjectStore, Depends()],
) -> list[ReadProject]:
    projects = await project_store.get_all()
    return projects


@router.post(
    "/",
    response_description="Create a new project",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_active_user)],
)
async def create_project(
    project: CreateProject,
    project_store: Annotated[ProjectStore, Depends()],
) -> ReadProject:
    new_project = await project_store.create(project)
    return new_project


@router.get(
    "/{project_id}",
    response_description="Get a single project",
    dependencies=[Depends(current_active_user)],
)
async def read_project(
    project_id: uuid.UUID,
    project_store: Annotated[ProjectStore, Depends()],
) -> ReadProject:
    project_entry = await project_store.get(project_id)
    return project_entry


@router.delete(
    "/{project_id}",
    response_description="Delete a single project",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: uuid.UUID,
    project_store: Annotated[ProjectStore, Depends()],
) -> None:
    await project_store.delete(project_id)
    return None


@router.patch(
    "/{project_id}",
    response_description="Update a single project",
    dependencies=[Depends(current_active_user)],
)
async def update_project(
    project_id: uuid.UUID,
    project: UpdateProject,
    project_store: Annotated[ProjectStore, Depends()],
) -> ReadProject:
    project_entry = await project_store.update(project_id, project)
    return project_entry
