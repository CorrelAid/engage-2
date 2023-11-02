import uuid
from collections import namedtuple
from datetime import datetime

import pytest
from api.app import app
from api.auth.users import current_active_user
from api.routers.comments import CommentStore, ReadComment
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
    MockedUser = namedtuple("MockedUser", ["id"])
    mocked_user = MockedUser(uuid.uuid4())

    app.dependency_overrides[current_active_user] = lambda: mocked_user
    yield
    del app.dependency_overrides[current_active_user]


class CommentDictStore:
    comments: dict[uuid.UUID, ReadComment] = {}

    async def get(self, comment_id):
        try:
            return self.comments[comment_id]
        except KeyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    async def get_all(self):
        return self.comments.values()

    async def create(self, comment, creator_id):
        comment_id = uuid.uuid4()
        processing_time = datetime.utcnow()

        comment_entry = ReadComment(
            **comment.model_dump(),
            id=comment_id,
            created_by=creator_id,
            created_at=processing_time,
            updated_at=processing_time,
            updated_by=creator_id,
        )
        self.comments[comment_id] = comment_entry
        return comment_entry

    async def update(self, comment_id, comment, updater_id):
        comment_entry = await self.get(comment_id)
        for key, value in comment.model_dump(exclude_defaults=True).items():
            if getattr(comment_entry, key) != value:
                setattr(comment_entry, key, value)
        comment_entry.updated_by = updater_id
        comment_entry.updated_at = datetime.utcnow()
        return comment_entry

    async def delete(self, comment_id):
        await self.get(comment_id)
        del self.comments[comment_id]
        return None


@pytest.fixture
def override_comment_store():
    app.dependency_overrides[CommentStore] = CommentDictStore
    yield
    del app.dependency_overrides[CommentStore]
