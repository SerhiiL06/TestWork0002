from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from backend.domain.ioc.providers import container
from backend.presentation.routers.auth import auth_router
from backend.presentation.routers.tasks import tasks_router
from backend.presentation.routers.users import users_router


def application() -> FastAPI:
    fastapi = FastAPI()

    fastapi.include_router(users_router)
    fastapi.include_router(tasks_router)
    fastapi.include_router(auth_router)

    setup_dishka(container, fastapi)

    return fastapi


app = application()
