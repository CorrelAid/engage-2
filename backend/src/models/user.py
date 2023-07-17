from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from models.base import Base
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Basic Userclass used for fast-api users extended with
    Correlaid attribute field to have all user data in one place.
    """

    name: Mapped[str] = mapped_column(String)
    roles: Mapped[list[str]] = mapped_column(ARRAY(String))


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass
