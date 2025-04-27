from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class DatabaseDTO:
    db: str
    username: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | None = None
    driver: str = "postgresql+asyncpg"
