from app.api.routers import user_management
from app.auth.users import current_active_user
from app.database.connection import create_db_and_tables
from app.database.models import User
from fastapi import Depends, FastAPI

app = FastAPI()

# All necessary endpoints for user management
app.include_router(user_management.auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_management.register_router, prefix="/auth", tags=["auth"])
app.include_router(user_management.reset_password_router, prefix="/auth", tags=["auth"])
app.include_router(user_management.verify_router, prefix="/auth", tags=["auth"])
app.include_router(user_management.get_users_router, prefix="/users", tags=["users"])


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
