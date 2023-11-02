from api.routers import auth, comments, organizations, projects
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from settings import settings


def custom_generate_unique_id(route: APIRoute):
    return route.name


app = FastAPI(generate_unique_id_function=custom_generate_unique_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth.router)
app.include_router(
    router=organizations.router, prefix="/organizations", tags=["organizations"]
)
app.include_router(router=projects.router, prefix="/projects", tags=["projects"])
app.include_router(router=comments.router, prefix="/comments", tags=["comments"])
