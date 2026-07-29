from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.config.database_settings import get_session
from fast_zero.tasks.models import Task
from fast_zero.tasks.schemas import TaskList, TaskPublic, TaskSchema, TaskUpdate
from fast_zero.users.models import User
from fast_zero.users.security import get_current_user

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TaskPublic)
async def create_task(
    task: TaskSchema,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    db_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=user.id,
    )
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


@router.get('/', response_model=TaskList)
async def list_tasks(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    title: str | None = None,
    description: str | None = None,
    state: str | None = None,
    offset: int = 0,
    limit: int = 100,
):
    query = select(Task).filter(Task.user_id == user.id)

    if title:
        query = query.filter(Task.title.contains(title))
    if description:
        query = query.filter(Task.description.contains(description))
    if state:
        query = query.filter(Task.state == state)

    result = await session.scalars(query.offset(offset).limit(limit))
    tasks = result.all()

    return {'tasks': tasks}


@router.patch('/{task_id}', response_model=TaskPublic)
async def patch_task(
    task_id: int,
    task: TaskUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    db_task = await session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )
    if not db_task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    await session.commit()
    await session.refresh(db_task)
    return db_task


@router.delete('/{task_id}', response_model=dict)
async def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    db_task = await session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )
    if not db_task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    await session.delete(db_task)
    await session.commit()

    return {'message': 'Task has been deleted successfully.'}