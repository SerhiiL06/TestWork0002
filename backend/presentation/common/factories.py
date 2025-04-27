from typing import Annotated

from fastapi import Depends

from backend.domain.ioc.providers import sync_container
from backend.domain.services.auth_service import AuthService


def current_user_factory():
    with sync_container() as cont:
        service = cont.get(AuthService)

    return Annotated[dict, Depends(service.authenticate)]


current_user = current_user_factory()
