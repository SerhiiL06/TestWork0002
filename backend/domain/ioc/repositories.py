from dishka import provide, Scope, Provider

from backend.domain.repositories.user_repo import UserRepository


class RepositoryProvider(Provider):
    component = "R"

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(self) -> UserRepository:
        return UserRepository()
