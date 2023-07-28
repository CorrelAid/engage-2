from typing import Annotated

from api.auth.users import current_active_user
from api.routers import auth, projects
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.user import User
from settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth.router)
app.include_router(router=projects.router, prefix="/projects", tags=["projects"])


@app.get("/authenticated-route")
async def authenticated_route(user: Annotated[User, Depends(current_active_user)]):
    return {"message": f"Hello {user.email}!"}
