from uuid import UUID

from api.auth.users import auth_backend, fastapi_users
from fastapi import APIRouter
from fastapi_users import schemas
from pydantic import Field

router = APIRouter(prefix="/auth", tags=["auth"])


router.include_router(router=fastapi_users.get_auth_router(backend=auth_backend))
router.include_router(router=fastapi_users.get_reset_password_router())


class UserCreate(schemas.BaseUserCreate):
    roles: list[str] = Field(default=["member"])
    name: str = Field(default=...)


class UserRead(schemas.BaseUser[UUID]):
    roles: list[str] = Field(default=["member"])
    name: str = Field(default=...)


class UserUpdate(schemas.BaseUserUpdate):
    roles: list[str] = ["member"]
    name: str = Field(default=...)


router.include_router(
    router=fastapi_users.get_register_router(
        user_schema=UserRead,
        user_create_schema=UserCreate,
    )
)
router.include_router(
    router=fastapi_users.get_verify_router(
        user_schema=UserRead,
    )
)
router.include_router(
    router=fastapi_users.get_users_router(
        user_schema=UserRead,
        user_update_schema=UserUpdate,
    )
)
