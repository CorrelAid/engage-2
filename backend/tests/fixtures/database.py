import contextlib
import uuid
from datetime import datetime
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from api.auth.users import get_user_manager
from api.routers.auth import UserCreate
from database.session import get_async_session, get_user_service
from models.comment import Comment
from models.project import Project
from models.user import User
from settings import settings
from sqlalchemy import delete, text

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_service_context = contextlib.asynccontextmanager(get_user_service)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


@pytest.fixture(scope="session")
def alembic_upgrade():
    if settings.tests.test_database and settings.tests.use_latest_migration:
        backend_root = Path(__file__).parent.parent.parent
        alembic_cfg = Config(backend_root / "src" / "alembic.ini")
        migration_directory = alembic_cfg.get_main_option("script_location")
        alembic_cfg.set_main_option(
            "script_location", str(backend_root / "src" / migration_directory)
        )
        command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session")
def admin_details():
    return {
        "name": "TEST",
        "email": "test@gmail.com",
        "password": "1234",
        "is_superuser": True,
        "roles": [],
    }


@pytest.fixture(scope="session", autouse=True)
async def admin_user(admin_details, alembic_upgrade):
    """Creates a user with admin privileges for testing purposes.

    The test does "tear down" up front because asyncio errors in tests
    can cause the regular tear down after the yield statement to not
    be executed. This approach is reliable, because delete statements
    in the database are idempotent and also succeed if the user does
    not exist.
    """
    if settings.tests.test_database:
        async with get_async_session_context() as session:
            delete_stmt = delete(User).where(User.email == admin_details.get("email"))
            await session.execute(delete_stmt)
            await session.commit()

            async with get_user_service_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(UserCreate(**admin_details))
            yield
    else:
        yield


@pytest.fixture(scope="session")
async def project_details():
    return {
        "title": "Test Project",
        "summary": "Test Summary",
        "status": "Test Status",
    }


@pytest.fixture(scope="session", autouse=True)
async def example_project(project_details, alembic_upgrade):
    if settings.tests.test_database:
        async with get_async_session_context() as session:
            delete_stmt = delete(Project).where(
                Project.title == project_details.get("title")
            )
            await session.execute(delete_stmt)
            await session.commit()

            project = Project(**project_details, id=uuid.uuid4())
            session.add(project)
            await session.commit()

            yield
    else:
        yield


@pytest.fixture(scope="session")
async def comment_details():
    return {
        "text": "This is a test comment!",
        "updated_at": datetime.utcnow(),
        "created_at": datetime.utcnow(),
    }


@pytest.fixture(scope="session", autouse=True)
async def example_comment(comment_details, alembic_upgrade):
    if settings.tests.test_database:
        async with get_async_session_context() as session:
            delete_stmt = delete(Comment).where(
                Comment.text == comment_details.get("text")
            )
            await session.execute(delete_stmt)
            await session.commit()

            # model based statment has issues with postgres system user table.
            # As a result we use a text query where we can quote the table.
            user = (await session.execute(text('select * from "user";'))).fetchone()

            comment = Comment(
                **comment_details,
                created_by=user.id,
                updated_by=user.id,
                id=uuid.uuid4(),
            )
            session.add(comment)
            await session.commit()

            yield

            delete_stmt = delete(Comment).where(
                Comment.text == comment_details.get("text")
            )
            await session.execute(delete_stmt)
            await session.commit()
    else:
        yield
