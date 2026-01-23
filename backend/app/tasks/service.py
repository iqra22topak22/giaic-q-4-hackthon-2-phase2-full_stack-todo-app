from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from app.models.task import Task, TaskCreate, TaskUpdate, TaskWithUserEmail
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


async def get_tasks_for_user_with_email(
    session: AsyncSession,
    user_id: str,
    completed: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0
):
    """Get all tasks for a specific user with user email."""
    # First, get the user to fetch their email
    user_query = select(User).where(User.id == user_id)
    user_result = await session.exec(user_query)
    user = user_result.first()
    user_email = user.email if user else None

    # Then get the tasks for the user
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    query = query.offset(offset).limit(limit)

    result = await session.exec(query)
    tasks = result.all()

    # Convert tasks to TaskWithUserEmail format
    tasks_with_email = []
    for task in tasks:
        task_with_email = TaskWithUserEmail(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_email=user_email
        )
        tasks_with_email.append(task_with_email)

    # Get total count for pagination metadata
    count_query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        count_query = count_query.where(Task.completed == completed)
    count_result = await session.exec(count_query)
    total_count = len(count_result.all())

    return tasks_with_email, total_count


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


async def create_multiple_tasks_for_user(session: AsyncSession, tasks_create: List[TaskCreate], user_id: str):
    """Create multiple tasks for a specific user."""
    created_tasks = []

    for task_create in tasks_create:
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id
        )

        session.add(db_task)
        created_tasks.append(db_task)

    await session.commit()

    # Refresh all created tasks to get their IDs and timestamps
    for task in created_tasks:
        await session.refresh(task)

    return created_tasks