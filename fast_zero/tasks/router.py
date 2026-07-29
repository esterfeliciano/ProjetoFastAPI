from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session  # Use Session síncrona do seu config

from fast_zero.config.database_settings import get_session
from fast_zero.tasks.models import Task
from fast_zero.tasks.schemas import (
    TaskFilter,
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)
from fast_zero.users.models import User
from fast_zero.users.security import get_current_user

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TaskPublic)
async def create_task(
    task: TaskSchema,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=user.id,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get('/', response_model=TaskList)
async def list_tasks(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    filters: TaskFilter = Depends(),
):
    query = select(Task).filter(Task.user_id == user.id)

    if filters.title:
        query = query.filter(Task.title.contains(filters.title))
    if filters.description:
        query = query.filter(Task.description.contains(filters.description))
    if filters.state:
        query = query.filter(Task.state == filters.state)

    result = session.scalars(query.offset(filters.offset).limit(filters.limit))
    tasks = result.all()

    return {'tasks': tasks}


@router.patch('/{task_id}', response_model=TaskPublic)
async def patch_task(
    task_id: int,
    task: TaskUpdate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )
    if not db_task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete('/{task_id}', response_model=dict)
async def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )
    if not db_task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(db_task)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}
