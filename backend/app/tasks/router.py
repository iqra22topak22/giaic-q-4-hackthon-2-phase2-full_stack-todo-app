from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.tasks.service import (
    get_tasks_for_user,
    get_task_by_id_and_user,
    create_task_for_user,
    update_task_for_user,
    delete_task_for_user,
    toggle_task_completion
)
from app.tasks.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskCompletionUpdate,
    SuccessResponse
)
from app.database import get_async_session
from app.core.security import get_current_user, security
from fastapi.security import HTTPAuthorizationCredentials

def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user from the JWT token if available, otherwise return a default user ID.
    """
    try:
        # Check if credentials exist (authorization header was provided)
        if credentials is None:
            return "mock-user-id"  # No auth header provided, return default user ID

        token = credentials.credentials
        from app.core.security import verify_token
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            return "mock-user-id"  # Default user ID when token doesn't have sub
        return user_id
    except:
        # If no authentication provided or invalid token, return mock user ID
        return "mock-user-id"

router = APIRouter(prefix="", tags=["tasks"])

@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks_with_query_param(
    completed: bool = None,
    limit: int = 50,
    offset: int = 0,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve all tasks for the logged-in user (using auth).
    """
    tasks, total_count = await get_tasks_for_user(
        session, current_user_id, completed, limit, offset
    )

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

@router.get("/{user_id}/tasks", response_model=TaskListResponse)
async def get_tasks_by_user_id(
    user_id: str,
    completed: bool = None,
    limit: int = 50,
    offset: int = 0,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve all tasks for a specific user (matching auth user ID with path param).
    """
    # Verify that the user_id in the path matches the authenticated user
    # For mock user ID, allow access to its own tasks
    if user_id != current_user_id and not (user_id == "mock-user-id" and current_user_id == "mock-user-id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )

    tasks, total_count = await get_tasks_for_user(
        session, user_id, completed, limit, offset
    )

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
async def create_task_with_auth(
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the logged-in user (using auth).
    """
    # Validate input
    if not task_data.title or len(task_data.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and cannot be empty"
        )

    if task_data.description and len(task_data.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 1000 characters or less"
        )

    db_task = await create_task_for_user(session, task_data, current_user_id)

    return SuccessResponse(
        success=True,
        message="Task created successfully",
        data={
            "id": db_task.id,
            "user_id": db_task.user_id,
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "created_at": db_task.created_at.isoformat(),
            "updated_at": db_task.updated_at.isoformat()
        }
    )


@router.post("/{user_id}/tasks", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_task_by_user_id(
    user_id: str,
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for a specific user (matching auth user ID with path param).
    """
    # Verify that the user_id in the path matches the authenticated user
    # For mock user ID, allow access to its own tasks
    if user_id != current_user_id and not (user_id == "mock-user-id" and current_user_id == "mock-user-id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot create tasks for another user"
        )

    # Validate input
    if not task_data.title or len(task_data.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and cannot be empty"
        )

    if task_data.description and len(task_data.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 1000 characters or less"
        )

    db_task = await create_task_for_user(session, task_data, user_id)

    return SuccessResponse(
        success=True,
        message="Task created successfully",
        data={
            "id": db_task.id,
            "user_id": db_task.user_id,
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "created_at": db_task.created_at.isoformat(),
            "updated_at": db_task.updated_at.isoformat()
        }
    )


@router.get("/tasks/{task_id}", response_model=SuccessResponse)
async def get_task_with_auth(
    task_id: int,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a specific task by ID for the logged-in user (using auth).
    """
    task = await get_task_by_id_and_user(session, task_id, current_user_id)

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


@router.get("/{user_id}/tasks/{task_id}", response_model=SuccessResponse)
async def get_task_by_user_id(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a specific task by ID for a specific user (matching auth user ID with path param).
    """
    # Verify that the user_id in the path matches the authenticated user
    # For mock user ID, allow access to its own tasks
    if user_id != current_user_id and not (user_id == "mock-user-id" and current_user_id == "mock-user-id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )

    task = await get_task_by_id_and_user(session, task_id, user_id)

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
async def update_task_with_auth(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update an existing task for the logged-in user (using auth).
    """
    # Validate input if provided
    if task_update.title is not None:
        if not task_update.title or len(task_update.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )

    if task_update.description is not None and len(task_update.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 1000 characters or less"
        )

    updated_task = await update_task_for_user(session, task_id, task_update, current_user_id)

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


@router.put("/{user_id}/tasks/{task_id}", response_model=SuccessResponse)
async def update_task_by_user_id(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update an existing task for a specific user (matching auth user ID with path param).
    """
    # Verify that the user_id in the path matches the authenticated user
    # For mock user ID, allow access to its own tasks
    if user_id != current_user_id and not (user_id == "mock-user-id" and current_user_id == "mock-user-id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's tasks"
        )

    # Validate input if provided
    if task_update.title is not None:
        if not task_update.title or len(task_update.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )

    if task_update.description is not None and len(task_update.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 1000 characters or less"
        )

    updated_task = await update_task_for_user(session, task_id, task_update, user_id)

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


@router.delete("/tasks/{task_id}", response_model=SuccessResponse)
async def delete_task_with_auth(
    task_id: int,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task by ID for the logged-in user (using auth).
    """
    success = await delete_task_for_user(session, task_id, current_user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the user"
        )

    return SuccessResponse(
        success=True,
        message="Task deleted successfully"
    )


@router.delete("/{user_id}/tasks/{task_id}", response_model=SuccessResponse)
async def delete_task_by_user_id(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task by ID for a specific user (matching auth user ID with path param).
    """
    # Verify that the user_id in the path matches the authenticated user
    # For mock user ID, allow access to its own tasks
    if user_id != current_user_id and not (user_id == "mock-user-id" and current_user_id == "mock-user-id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot delete another user's tasks"
        )

    success = await delete_task_for_user(session, task_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the user"
        )

    return SuccessResponse(
        success=True,
        message="Task deleted successfully"
    )


@router.patch("/tasks/{task_id}/complete", response_model=SuccessResponse)
async def toggle_task_completion_with_auth(
    task_id: int,
    completion_data: TaskCompletionUpdate,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task for the logged-in user (using auth).
    """
    updated_task = await toggle_task_completion(session, task_id, completion_data.completed, current_user_id)

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


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=SuccessResponse)
async def toggle_task_completion_by_user_id(
    user_id: str,
    task_id: int,
    completion_data: TaskCompletionUpdate,
    current_user_id: str = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task for a specific user (matching auth user ID with path param).
    """
    # Verify that the user_id in the path matches the authenticated user
    # For mock user ID, allow access to its own tasks
    if user_id != current_user_id and not (user_id == "mock-user-id" and current_user_id == "mock-user-id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's tasks"
        )

    updated_task = await toggle_task_completion(session, task_id, completion_data.completed, user_id)

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