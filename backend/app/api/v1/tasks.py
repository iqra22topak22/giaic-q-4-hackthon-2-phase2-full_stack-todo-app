from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from app.models.task import Task, TaskCreate, TaskUpdate
from app.schemas.task import (
    TaskCreate as TaskCreateSchema,
    TaskUpdate as TaskUpdateSchema,
    TaskResponse,
    TaskListResponse,
    TaskCompletionUpdate,
    SuccessResponse,
    ErrorResponse
)
from app.api.deps import get_db_session
from app.utils.validators import validate_task_title, validate_task_description
from app.config import settings
from app.auth import get_authenticated_user_id, get_authenticated_user_id_from_path
from app.in_memory_db import (
    get_tasks_for_user, add_task_for_user, get_task_for_user,
    update_task_for_user, delete_task_for_user
)
from datetime import datetime

router = APIRouter()

@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    request: Request,
    user_id: str = Path(..., description="The user's ID"),
    authenticated_user_id: str = Depends(get_authenticated_user_id_from_path),
    db: AsyncSession = Depends(get_db_session),
    completed: bool = Query(None, description="Filter tasks by completion status"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip")
):
    """
    Retrieve all tasks for the specified user.
    """
    # Use the authenticated user ID which handles dev/prod differences
    validated_user_id = authenticated_user_id

    if settings.ENVIRONMENT == "development":
        # Use in-memory storage in development
        tasks = get_tasks_for_user(validated_user_id)

        # Apply completion filter if specified
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        # Apply pagination
        start_idx = offset
        end_idx = offset + limit
        paginated_tasks = tasks[start_idx:end_idx]
        total_count = len(tasks)

        # Convert to response format
        task_responses = [
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in paginated_tasks
        ]

        return TaskListResponse(
            tasks=task_responses,
            total_count=total_count,
            limit=limit,
            offset=offset
        )
    else:
        # Use database in production
        # Build query with user_id filter
        query = select(Task).where(Task.user_id == validated_user_id)

        # Apply completion filter if specified
        if completed is not None:
            query = query.where(Task.completed == completed)

        # Apply pagination
        query = query.offset(offset).limit(limit)

        result = await db.exec(query)
        tasks = result.all()

        # Get total count for pagination metadata
        count_query = select(Task).where(Task.user_id == validated_user_id)
        if completed is not None:
            count_query = count_query.where(Task.completed == completed)
        count_result = await db.exec(count_query)
        total_count = len(count_result.all())

        # Convert to response format
        task_responses = [
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]

        return TaskListResponse(
            tasks=task_responses,
            total_count=total_count,
            limit=limit,
            offset=offset
        )


@router.post("/tasks", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: Request,
    task_data: TaskCreateSchema,
    user_id: str = Path(..., description="The user's ID"),
    authenticated_user_id: str = Depends(get_authenticated_user_id_from_path),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new task for the specified user.
    """
    # Use the authenticated user ID which handles dev/prod differences
    validated_user_id = authenticated_user_id

    # Validate input
    if not validate_task_title(task_data.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be between 1 and 255 characters"
        )

    if not validate_task_description(task_data.description):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 1000 characters or less"
        )

    # Create task object
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=getattr(task_data, 'completed', False),
        user_id=validated_user_id
    )

    if settings.ENVIRONMENT == "development":
        # Use in-memory storage in development
        saved_task = add_task_for_user(validated_user_id, task)

        return SuccessResponse(
            success=True,
            message="Task created successfully",
            data={
                "id": saved_task.id,
                "user_id": saved_task.user_id,
                "title": saved_task.title,
                "description": saved_task.description,
                "completed": saved_task.completed,
                "created_at": saved_task.created_at.isoformat(),
                "updated_at": saved_task.updated_at.isoformat()
            }
        )
    else:
        # Use database in production
        # Add to database
        db.add(task)
        await db.commit()
        await db.refresh(task)

        return SuccessResponse(
            success=True,
            message="Task created successfully",
            data={
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        )


@router.get("/tasks/{task_id}", response_model=SuccessResponse)
async def get_task(
    request: Request,
    task_id: int,
    user_id: str = Path(..., description="The user's ID"),
    authenticated_user_id: str = Depends(get_authenticated_user_id_from_path),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve a specific task by ID for the specified user.
    """
    # Use the authenticated user ID which handles dev/prod differences
    validated_user_id = authenticated_user_id

    if settings.ENVIRONMENT == "development":
        # Use in-memory storage in development
        task = get_task_for_user(validated_user_id, task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the user"
            )

        return SuccessResponse(
            success=True,
            data={
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        )
    else:
        # Use database in production
        # Query for the task with user_id filter to ensure ownership
        result = await db.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == validated_user_id)
        )
        task = result.first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the user"
            )

        return SuccessResponse(
            success=True,
            data={
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        )


@router.put("/tasks/{task_id}", response_model=SuccessResponse)
async def update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdateSchema,
    user_id: str = Path(..., description="The user's ID"),
    authenticated_user_id: str = Depends(get_authenticated_user_id_from_path),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update an existing task for the specified user.
    """
    # Use the authenticated user ID which handles dev/prod differences
    validated_user_id = authenticated_user_id

    # Create a temporary task object for validation
    temp_task = Task(
        title=task_update.title,
        description=task_update.description,
        completed=task_update.completed,
        user_id=validated_user_id
    )

    # Validate input if provided
    if task_update.title is not None:
        if not validate_task_title(task_update.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be between 1 and 255 characters"
            )

    if task_update.description is not None:
        if not validate_task_description(task_update.description):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be 1000 characters or less"
            )

    if settings.ENVIRONMENT == "development":
        # Use in-memory storage in development
        existing_task = get_task_for_user(validated_user_id, task_id)

        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the user"
            )

        # Update the task properties
        if task_update.title is not None:
            existing_task.title = task_update.title
        if task_update.description is not None:
            existing_task.description = task_update.description
        if task_update.completed is not None:
            existing_task.completed = task_update.completed

        # Update the updated_at timestamp
        existing_task.updated_at = datetime.utcnow()

        # Update the task in memory
        updated_task = update_task_for_user(validated_user_id, task_id, existing_task)

        return SuccessResponse(
            success=True,
            message="Task updated successfully",
            data={
                "id": updated_task.id,
                "user_id": updated_task.user_id,
                "title": updated_task.title,
                "description": updated_task.description,
                "completed": updated_task.completed,
                "created_at": updated_task.created_at.isoformat(),
                "updated_at": updated_task.updated_at.isoformat()
            }
        )
    else:
        # Use database in production
        # Query for the task with user_id filter to ensure ownership
        result = await db.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == validated_user_id)
        )
        task = result.first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the user"
            )

        # Validate input if provided
        if task_update.title is not None:
            if not validate_task_title(task_update.title):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title must be between 1 and 255 characters"
                )
            task.title = task_update.title

        if task_update.description is not None:
            if not validate_task_description(task_update.description):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Description must be 1000 characters or less"
                )
            task.description = task_update.description

        if task_update.completed is not None:
            task.completed = task_update.completed

        # Update the updated_at timestamp
        task.updated_at = datetime.utcnow()

        # Commit changes
        db.add(task)
        await db.commit()
        await db.refresh(task)

        return SuccessResponse(
            success=True,
            message="Task updated successfully",
            data={
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        )


@router.delete("/tasks/{task_id}", response_model=SuccessResponse)
async def delete_task(
    request: Request,
    task_id: int,
    user_id: str = Path(..., description="The user's ID"),
    authenticated_user_id: str = Depends(get_authenticated_user_id_from_path),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific task by ID for the specified user.
    """
    # Use the authenticated user ID which handles dev/prod differences
    validated_user_id = authenticated_user_id

    if settings.ENVIRONMENT == "development":
        # Use in-memory storage in development
        success = delete_task_for_user(validated_user_id, task_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the user"
            )

        return SuccessResponse(
            success=True,
            message="Task deleted successfully"
        )
    else:
        # Use database in production
        # Query for the task with user_id filter to ensure ownership
        result = await db.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == validated_user_id)
        )
        task = result.first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the user"
            )

        # Delete the task
        await db.delete(task)
        await db.commit()

        return SuccessResponse(
            success=True,
            message="Task deleted successfully"
        )


@router.patch("/tasks/{task_id}/complete", response_model=SuccessResponse)
async def toggle_task_completion(
    request: Request,
    task_id: int,
    completion_data: TaskCompletionUpdate,
    user_id: str = Path(..., description="The user's ID"),
    authenticated_user_id: str = Depends(get_authenticated_user_id_from_path),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Toggle the completion status of a specific task for the specified user.
    """
    # Use the authenticated user ID which handles dev/prod differences
    validated_user_id = authenticated_user_id

    if settings.ENVIRONMENT == "development":
        # Use in-memory storage in development
        existing_task = get_task_for_user(validated_user_id, task_id)

        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the user"
            )

        # Update the completion status
        existing_task.completed = completion_data.completed
        existing_task.updated_at = datetime.utcnow()

        # Update the task in memory
        updated_task = update_task_for_user(validated_user_id, task_id, existing_task)

        return SuccessResponse(
            success=True,
            message="Task completion status updated successfully",
            data={
                "id": updated_task.id,
                "user_id": updated_task.user_id,
                "title": updated_task.title,
                "description": updated_task.description,
                "completed": updated_task.completed,
                "created_at": updated_task.created_at.isoformat(),
                "updated_at": updated_task.updated_at.isoformat()
            }
        )
    else:
        # Use database in production
        # Query for the task with user_id filter to ensure ownership
        result = await db.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == validated_user_id)
        )
        task = result.first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the user"
            )

        # Update the completion status
        task.completed = completion_data.completed
        task.updated_at = datetime.utcnow()

        # Commit changes
        db.add(task)
        await db.commit()
        await db.refresh(task)

        return SuccessResponse(
            success=True,
            message="Task completion status updated successfully",
            data={
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        )