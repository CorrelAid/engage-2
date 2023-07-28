import uuid

import pytest
from api.app import app
from api.auth.users import current_active_user
from api.routers.projects import ProjectStore, ReadProject
from fastapi import HTTPException, status


class ProjectDictStore:
    projects: dict[uuid.UUID, ReadProject] = {}

    async def get(self, project_id):
        try:
            return self.projects[project_id]
        except KeyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    async def get_all(self):
        return self.projects.values()

    async def create(self, project):
        project_id = uuid.uuid4()
        project_entry = ReadProject(**project.model_dump(), id=project_id)
        self.projects[project_id] = project_entry
        return project_entry

    async def update(self, project_id, project):
        project_entry = await self.get(project_id)
        project_entry.title = project.title
        project_entry.summary = project.summary
        project_entry.status = project.status
        return project_entry

    async def delete(self, project_id):
        await self.get(project_id)
        del self.projects[project_id]
        return None


@pytest.fixture
def override_project_store():
    app.dependency_overrides[ProjectStore] = ProjectDictStore
    yield
    del app.dependency_overrides[ProjectStore]


@pytest.fixture
def override_active_user():
    app.dependency_overrides[current_active_user] = lambda: {}
    yield
    del app.dependency_overrides[current_active_user]
