from dishka import make_async_container, make_container

from backend.domain.ioc.config import ConfigProvider
from backend.domain.ioc.database import DatabaseProvider
from backend.domain.ioc.repositories import RepositoryProvider
from backend.domain.ioc.services import ServiceProvider
from backend.domain.ioc.session import SessionProvider

container = make_async_container(
    DatabaseProvider(),
    SessionProvider(),
    RepositoryProvider(),
    ServiceProvider(),
    ConfigProvider(),
)


sync_container = make_container(
    DatabaseProvider(),
    SessionProvider(),
    RepositoryProvider(),
    ServiceProvider(),
    ConfigProvider(),
)
