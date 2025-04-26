from dataclasses import dataclass

from backend.common.enums import TaskStatus


@dataclass
class CreateTask:
    title: str
    priority: int
    description: str | None = None


@dataclass
class UpdateTask:
    title: str | None = None
    description: str | None = None
    priority: int | None = None
    status: TaskStatus | None = None
