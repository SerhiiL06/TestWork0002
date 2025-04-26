from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class DatabaseDTO:
    db: str
    username: str
    password: str
    host: str
    port: int
    driver: str = "postgresql+asyncpg"
