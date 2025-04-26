from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infra.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(String(320), unique=True)
    hashed_password: Mapped[str]

    joined_at: Mapped[datetime] = mapped_column(default=datetime.now())

    def __repr__(self) -> str:
        return self.email
