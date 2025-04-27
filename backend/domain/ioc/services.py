from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from passlib.context import CryptContext

from backend.domain.repositories.task_repo import TaskRepository
from backend.domain.repositories.user_repo import UserRepository
from backend.domain.services.auth_service import AuthService
from backend.domain.services.password_service import PasswordService
from backend.domain.services.task_service import TaskService
from backend.domain.services.token_service import TokenService
from backend.domain.services.user_service import UserService


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_bcrypt_context(self) -> CryptContext:
        return CryptContext(schemes=["bcrypt"])

    @provide(scope=Scope.REQUEST)
    def provide_password_service(self, bcrypt_context: CryptContext) -> PasswordService:
        return PasswordService(bcrypt_context)

    @provide(scope=Scope.REQUEST)
    def provide_users_service(
        self, repo: Annotated[UserRepository, FromComponent("R")]
    ) -> UserService:
        return UserService(repo)

    @provide(scope=Scope.REQUEST)
    def provide_token_service(self) -> TokenService:
        return TokenService()

    @provide(scope=Scope.REQUEST)
    def provide_auth_service(
        self,
        repo: Annotated[UserRepository, FromComponent("R")],
        password_service: PasswordService,
        token_service: TokenService,
    ) -> AuthService:
        return AuthService(repo, password_service, token_service)

    @provide(scope=Scope.REQUEST)
    def provide_task_service(
        self, repo: Annotated[TaskRepository, FromComponent("R")]
    ) -> TaskService:
        return TaskService(repo)
