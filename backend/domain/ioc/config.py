from dishka import Provider, provide, Scope

from backend.infra.settings import Settings


class ConfigProvider(Provider):
    component = "C"

    @provide(scope=Scope.APP)
    def provide_config(self) -> Settings:
        return Settings()
