from app.api.schemas import UserCreate, UserRead, UserUpdate
from app.auth.users import auth_backend, fastapi_users

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
reset_password_router = fastapi_users.get_reset_password_router()
verify_router = fastapi_users.get_verify_router(UserRead)
get_users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
