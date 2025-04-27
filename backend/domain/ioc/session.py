from typing import Annotated, AsyncGenerator

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infra.database.connection import DatabaseCORE


class SessionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self, database: Annotated[DatabaseCORE, FromComponent("D")]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with database.session_transaction() as session:
            yield session
