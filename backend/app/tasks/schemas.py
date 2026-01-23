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


class TaskWithUserEmailResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_email: Optional[str] = None


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total_count: int
    limit: int
    offset: int


class TaskListWithUserEmailResponse(BaseModel):
    tasks: List[TaskWithUserEmailResponse]
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


class BulkTaskCreateRequest(BaseModel):
    tasks: List[TaskCreate]


class BulkTaskCreateResponse(BaseModel):
    success: bool
    message: str
    data: List[TaskResponse]