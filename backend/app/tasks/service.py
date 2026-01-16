from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from app.models.task import Task, TaskCreate, TaskUpdate
from app.models.user import User
from fastapi import HTTPException, status


async def get_tasks_for_user(
    session: AsyncSession,
    user_id: str,
    completed: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0
):
    """Get all tasks for a specific user."""
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    query = query.offset(offset).limit(limit)

    result = await session.exec(query)
    tasks = result.all()

    # Get total count for pagination metadata
    count_query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        count_query = count_query.where(Task.completed == completed)
    count_result = await session.exec(count_query)
    total_count = len(count_result.all())

    return tasks, total_count


async def get_task_by_id_and_user(session: AsyncSession, task_id: int, user_id: str):
    """Get a specific task by ID for a specific user."""
    query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    result = await session.exec(query)
    task = result.first()
    return task


async def create_task_for_user(session: AsyncSession, task_create: TaskCreate, user_id: str):
    """Create a new task for a specific user."""
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=user_id
    )

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


async def update_task_for_user(session: AsyncSession, task_id: int, task_update: TaskUpdate, user_id: str):
    """Update a specific task for a specific user."""
    db_task = await get_task_by_id_and_user(session, task_id, user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the user"
        )

    # Update the task with provided values
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    await session.commit()
    await session.refresh(db_task)

    return db_task


async def delete_task_for_user(session: AsyncSession, task_id: int, user_id: str):
    """Delete a specific task for a specific user."""
    db_task = await get_task_by_id_and_user(session, task_id, user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the user"
        )

    await session.delete(db_task)
    await session.commit()

    return True


async def toggle_task_completion(session: AsyncSession, task_id: int, completed: bool, user_id: str):
    """Toggle the completion status of a specific task for a specific user."""
    db_task = await get_task_by_id_and_user(session, task_id, user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the user"
        )

    db_task.completed = completed

    await session.commit()
    await session.refresh(db_task)

    return db_task