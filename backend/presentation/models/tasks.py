from dataclasses import dataclass

from backend.common.enums import TaskStatus


@dataclass
class CreateTask:
    title: str
    priority: int
    description: str | None = None


@dataclass
class UpdateTask:
    id: int
    title: str
    priority: int
    status: TaskStatus
    description: str | None = None
