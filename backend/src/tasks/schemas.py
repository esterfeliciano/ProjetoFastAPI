from src.tasks.models import TaskState
from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    description: str
    state: TaskState


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None


class TaskPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TaskState


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class TaskFilter(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None
    offset: int = 0
    limit: int = 100
