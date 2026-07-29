from pydantic import BaseModel

from fast_zero.tasks.models import TaskState


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
