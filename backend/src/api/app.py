from api.routers import auth
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from settings import settings
from starlette import status
from starlette_csrf import CSRFMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    middleware_class=CSRFMiddleware,
    secret=settings.api.csrf_secret.get_secret_value(),
    cookie_secure=settings.api.cookie_secure,
)

app.include_router(router=auth.router)


@app.get(path="/csrf", status_code=status.HTTP_204_NO_CONTENT, tags=["csrf"])
async def get_csrf():
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
