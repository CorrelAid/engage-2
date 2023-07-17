import argparse
import asyncio
import contextlib
import logging
import sys

from app.api.schemas import UserCreate
from app.auth.users import get_user_manager
from app.database.connection import get_async_session, get_user_db
from fastapi_users.exceptions import UserAlreadyExists

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="CLI")

logger = logging.getLogger(__name__)


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="CLI")


async def adduser(
    email: str,
    password: str,
    is_superuser: bool,
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=is_superuser
                        )
                    )
                    logging.info(f"User created {user}")
    except UserAlreadyExists:
        logging.error(f"User {email} already exists")


add_user_parser = subparsers.add_parser("adduser")
add_user_parser.add_argument(
    "-e", "--email", dest="email", default="testuser@example.com"
)
add_user_parser.add_argument(
    "-p", "--password", dest="password", default="testpassword123"
)
add_user_parser.add_argument("-s", "--superuser", dest="is_superuser", default=False)
add_user_parser.set_defaults(func=adduser)


if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
    if args.func:
        if asyncio.iscoroutinefunction(args.func):
            asyncio.run(
                args.func(
                    args.email,
                    args.password,
                    args.is_superuser,
                )
            )
        else:
            args.func(args)
