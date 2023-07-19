import contextlib

import pytest
from api.auth.users import get_user_manager
from api.routers.auth import UserCreate
from database.session import get_async_session, get_user_service
from models.user import User
from sqlalchemy import delete

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_service_context = contextlib.asynccontextmanager(get_user_service)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


@pytest.fixture(scope="session")
def admin_details():
    return {
        "name": "TEST",
        "email": "test@gmail.com",
        "password": "1234",
        "is_superuser": True,
    }


@pytest.fixture(scope="session", autouse=True)
async def admin_user(admin_details):
    """Creates a user with admin privileges for testing purposes.

    The test does "tear down" up front because asyncio errors in tests
    can cause the regular tear down after the yield statement to not
    be executed. This approach is reliable, because delete statements
    in the database are idempotent and also succeed if the user does
    not exist.
    """
    async with get_async_session_context() as session:
        delete_stmt = delete(User).where(User.email == admin_details.get("email"))
        await session.execute(delete_stmt)
        await session.commit()

        async with get_user_service_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                await user_manager.create(UserCreate(**admin_details))
        yield
