from typing import Annotated

from dishka import Provider, Scope, provide, FromComponent

from backend.common.models import DatabaseDTO
from backend.infra.database.connection import DatabaseCORE
from backend.infra.settings import Settings


class DatabaseProvider(Provider):
    component = "D"

    @provide(scope=Scope.APP)
    def postgres_database_data(
        self, settings: Annotated[Settings, FromComponent("C")]
    ) -> DatabaseDTO:
        return DatabaseDTO(
            driver="postgresql+asyncpg",
            db=settings.POSTGRES_DB,
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=int(settings.POSTGRES_PORT),
        )

    @provide(scope=Scope.APP)
    def provide_database(self, db_data: DatabaseDTO) -> DatabaseCORE:
        return DatabaseCORE(
            db_data.driver,
            db_data.db,
            db_data.username,
            db_data.password,
            db_data.host,
            db_data.port,
        )
