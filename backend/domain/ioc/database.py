from dishka import Provider, Scope, provide

from backend.common.models import DatabaseDTO
from backend.infra.database.connection import DatabaseCORE
from backend.infra.settings import env_config


class DatabaseProvider(Provider):
    component = "D"

    @provide(scope=Scope.APP)
    def postgres_database_data(self) -> DatabaseDTO:
        return DatabaseDTO(
            driver="postgresql+asyncpg",
            db=env_config.POSTGRES_DB,
            username=env_config.POSTGRES_USERNAME,
            password=env_config.POSTGRES_PASSWORD,
            host=env_config.POSTGRES_HOST,
            port=env_config.POSTGRES_PORT,
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
