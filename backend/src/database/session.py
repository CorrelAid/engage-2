from typing import AsyncGenerator, AsyncIterator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from models.user import AccessToken, User
from settings import settings
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(url=settings.database.dsn)
# TODO(KW): Consider renaming this in accordance with the SQLAlchemy
# conventions. In their docs they use Pascal Case for session maker instances and don't
# include "maker" in the name to reflect that these instances are used similarly
# to SQLAlchemy's Session classes.
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except DatabaseError:
            await session.rollback()
            raise


async def get_user_service(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_service(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


async def transactional_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker.begin() as session:
        yield session
