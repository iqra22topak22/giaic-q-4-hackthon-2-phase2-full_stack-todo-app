from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    title: str  # Required field


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total_count: int
    limit: int
    offset: int


class TaskCompletionUpdate(BaseModel):
    completed: bool


class SuccessResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool
    error: dict