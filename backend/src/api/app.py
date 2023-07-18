from typing import Annotated

from api.auth.users import current_active_user
from api.routers import auth
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.user import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth.router)


@app.get("/authenticated-route")
async def authenticated_route(user: Annotated[User, Depends(current_active_user)]):
    return {"message": f"Hello {user.email}!"}
