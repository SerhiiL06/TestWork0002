import pytest_asyncio
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport
from pytest import fixture
from sqlalchemy import URL, create_engine

from backend.domain.ioc.repositories import RepositoryProvider
from backend.domain.ioc.services import ServiceProvider
from backend.domain.ioc.session import SessionProvider
from backend.infra.database.models.base import Base
from backend.presentation.routers.auth import auth_router
from backend.presentation.routers.tasks import tasks_router
from backend.presentation.routers.users import users_router
from tests.common.providers import MockDatabaseProvider


@fixture(scope="session", autouse=True)
def setup_db():
    db_url = URL.create(drivername="sqlite", database="test.sqlite3")
    test_engine = create_engine(db_url)

    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


@pytest_asyncio.fixture(autouse=True, scope="session")
async def dishka():
    container = make_async_container(
        MockDatabaseProvider(),
        SessionProvider(),
        ServiceProvider(),
        RepositoryProvider(),
    )
    yield container
    await container.close()


@fixture(scope="session", autouse=True)
def app(dishka: AsyncContainer) -> FastAPI:
    app_ = FastAPI()
    app_.include_router(users_router)
    app_.include_router(auth_router)
    app_.include_router(tasks_router)
    setup_dishka(dishka, app_)
    return app_


@fixture
def user() -> dict:
    return {
        "name": "test",
        "email": "test@gmail.com",
        "password_1": "string_1",
        "password_2": "string_1",
    }


@fixture
def transport(app: FastAPI) -> ASGITransport:
    return ASGITransport(app)
