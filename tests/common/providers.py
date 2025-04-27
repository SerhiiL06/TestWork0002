from dishka import Provider, Scope, provide

from backend.common.models import DatabaseDTO
from backend.infra.database.connection import DatabaseCORE


class MockDatabaseProvider(Provider):
    component = "D"

    @provide(scope=Scope.APP)
    def postgres_database_data(self) -> DatabaseDTO:
        return DatabaseDTO(driver="sqlite+aiosqlite", db="test.sqlite3")

    @provide(scope=Scope.APP)
    def provide_database(self, db_data: DatabaseDTO) -> DatabaseCORE:
        return DatabaseCORE(db_data.driver, db_data.db)
