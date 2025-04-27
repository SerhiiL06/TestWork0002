import pytest_asyncio
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from pytest import fixture

from backend.domain.ioc.repositories import RepositoryProvider
from backend.domain.ioc.services import ServiceProvider
from backend.domain.ioc.session import SessionProvider
from backend.infra.database.models.base import Base
from backend.presentation.routers.auth import auth_router
from backend.presentation.routers.users import users_router
from tests.database import test_core, test_engine
from tests.providers import MockDatabaseProvider


@fixture(scope="session", autouse=True)
def setup_db():
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
def app(dishka: AsyncContainer):
    app_ = FastAPI()
    app_.include_router(users_router)
    app_.include_router(auth_router)
    setup_dishka(dishka, app_)
    return app_


@pytest_asyncio.fixture(autouse=True)
async def session():
    async with test_core.session_transaction() as session:
        yield session
