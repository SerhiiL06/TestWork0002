from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class TaskFilter:
    status: Literal["PENDING", "DONE"] | None = None
    priority: int | None = None
    date_gte: datetime | None = None
    date_lte: datetime | None = None
