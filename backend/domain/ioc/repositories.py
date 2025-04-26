from dishka import provide, Scope, Provider

from backend.domain.repositories.task_repo import TaskRepository
from backend.domain.repositories.user_repo import UserRepository


class RepositoryProvider(Provider):
    component = "R"

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(self) -> UserRepository:
        return UserRepository()

    @provide(scope=Scope.REQUEST)
    def provide_task_repository(self) -> TaskRepository:
        return TaskRepository()
