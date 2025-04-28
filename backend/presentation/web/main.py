from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from backend.domain import exceptions as ext
from backend.domain.ioc.providers import container
from backend.presentation.routers.auth import auth_router
from backend.presentation.routers.tasks import tasks_router
from backend.presentation.routers.users import users_router


def application() -> FastAPI:
    fastapi = FastAPI()

    fastapi.include_router(users_router)
    fastapi.include_router(tasks_router)
    fastapi.include_router(auth_router)

    fastapi.add_exception_handler(
        ext.UserAlreadyExists, ext.user_already_exists_handler
    )
    fastapi.add_exception_handler(ext.UserNotFound, ext.user_not_found_handler)
    fastapi.add_exception_handler(ext.PermissionDenied, ext.permission_denied_handler)
    fastapi.add_exception_handler(ext.Unauthorized, ext.unauthorized_handler)

    setup_dishka(container, fastapi)

    return fastapi


app = application()
