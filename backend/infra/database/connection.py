from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DatabaseCORE:
    def __init__(
        self,
        driver: str,
        db_name: str,
        username: str = None,
        password: str = None,
        host: str = None,
        port: str | int = None,
    ) -> None:
        self._db_url = URL.create(
            drivername=driver,
            username=username,
            password=password,
            host=host,
            port=port,
            database=db_name,
        )
        self._engine = create_async_engine(self._db_url, pool_size=10, max_overflow=5)
        self.session_factory = async_sessionmaker(
            bind=self._engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def session_transaction(self) -> AsyncGenerator:
        async with self.session_factory() as conn:
            yield conn
