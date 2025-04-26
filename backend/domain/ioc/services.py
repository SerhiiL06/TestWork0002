from typing import Annotated

from dishka import Provider, provide, Scope, FromComponent
from passlib.context import CryptContext

from backend.domain.repositories.user_repo import UserRepository
from backend.domain.services.password_service import PasswordService
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
