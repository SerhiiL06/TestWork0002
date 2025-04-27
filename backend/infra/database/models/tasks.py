from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.enums import TaskStatus
from backend.infra.database.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

    status: Mapped[ENUM] = mapped_column(ENUM(TaskStatus), default=TaskStatus.PENDING)
    priority: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
