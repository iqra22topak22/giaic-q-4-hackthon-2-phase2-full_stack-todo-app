from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime
from typing import List, Optional

# Simple in-memory storage for demo purposes
tasks_storage = []

class Task:
    def __init__(self, id: int, title: str, description: str, completed: bool, user_id: str):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

app = FastAPI(
    title="Todo API - Demo Mode",
    description="Backend API for the Todo Web Application (Demo)",
    version="1.0.0"
)

# Configure CORS middleware
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "https://full-stack-todo-iqra22topak22s-projects.vercel.app",
    "https://full-stack-todo-cxdbrdr8s-iqra22topak22s-projects.vercel.app",
    "https://full-stack-todo-eta.vercel.app",
    "https://full-stack-todo-qfzzohhhm-iqra22topak22s-projects.vercel.app",
    "https://full-stack-todo-pqznvemgs-iqra22topak22s-projects.vercel.app",
    "https://full-stack-todo-dtleggcil-iqra22topak22s-projects.vercel.app",
    "https://full-stack-todo-qoyoy4yzl-iqra22topak22s-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Task schemas (simplified for demo)
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total_count: int
    limit: int
    offset: int

class SuccessResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None

class BulkTaskCreateRequest(BaseModel):
    tasks: List[TaskCreate]

class BulkTaskCreateResponse(BaseModel):
    success: bool
    message: str
    data: List[TaskResponse]

# Helper function to convert internal task to response
def task_to_response(task: Task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

# Mock user ID for demo
MOCK_USER_ID = "demo-user-12345"

@app.get("/")
def read_root():
    return {"status": "Backend is running successfully (Demo Mode)"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running successfully (Demo Mode)"}

# Tasks API endpoints
@app.get("/api/tasks", response_model=TaskListResponse)
async def get_tasks_with_query_param(
    completed: bool = None,
    limit: int = 50,
    offset: int = 0
):
    user_tasks = [task for task in tasks_storage if task.user_id == MOCK_USER_ID]
    
    if completed is not None:
        user_tasks = [task for task in user_tasks if task.completed == completed]
    
    # Apply pagination
    paginated_tasks = user_tasks[offset:offset + limit]
    
    task_responses = [task_to_response(task) for task in paginated_tasks]
    
    return TaskListResponse(
        tasks=task_responses,
        total_count=len(user_tasks),
        limit=limit,
        offset=offset
    )

@app.get("/api/{user_id}/tasks", response_model=TaskListResponse)
async def get_tasks_by_user_id(
    user_id: str,
    completed: bool = None,
    limit: int = 50,
    offset: int = 0
):
    # For demo, we'll just check if it's the mock user
    if user_id != MOCK_USER_ID:
        return TaskListResponse(tasks=[], total_count=0, limit=limit, offset=offset)
    
    user_tasks = [task for task in tasks_storage if task.user_id == user_id]
    
    if completed is not None:
        user_tasks = [task for task in user_tasks if task.completed == completed]
    
    # Apply pagination
    paginated_tasks = user_tasks[offset:offset + limit]
    
    task_responses = [task_to_response(task) for task in paginated_tasks]
    
    return TaskListResponse(
        tasks=task_responses,
        total_count=len(user_tasks),
        limit=limit,
        offset=offset
    )

@app.post("/api/tasks", response_model=SuccessResponse)
async def create_task_with_auth(task_data: TaskCreate):
    new_task = Task(
        id=len(tasks_storage) + 1,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=MOCK_USER_ID
    )
    
    tasks_storage.append(new_task)
    
    return SuccessResponse(
        success=True,
        message="Task created successfully",
        data={
            "id": new_task.id,
            "user_id": new_task.user_id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed,
            "created_at": new_task.created_at.isoformat(),
            "updated_at": new_task.updated_at.isoformat()
        }
    )

@app.post("/api/{user_id}/tasks", response_model=SuccessResponse)
async def create_task_by_user_id(user_id: str, task_data: TaskCreate):
    if user_id != MOCK_USER_ID:
        return SuccessResponse(success=False, message="Access denied")
    
    new_task = Task(
        id=len(tasks_storage) + 1,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_id
    )
    
    tasks_storage.append(new_task)
    
    return SuccessResponse(
        success=True,
        message="Task created successfully",
        data={
            "id": new_task.id,
            "user_id": new_task.user_id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed,
            "created_at": new_task.created_at.isoformat(),
            "updated_at": new_task.updated_at.isoformat()
        }
    )

@app.post("/api/tasks/bulk", response_model=BulkTaskCreateResponse)
async def create_multiple_tasks_with_auth(bulk_request: BulkTaskCreateRequest):
    created_tasks = []
    
    for task_create in bulk_request.tasks:
        new_task = Task(
            id=len(tasks_storage) + 1,
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=MOCK_USER_ID
        )
        
        tasks_storage.append(new_task)
        created_tasks.append(task_to_response(new_task))
    
    return BulkTaskCreateResponse(
        success=True,
        message=f"{len(created_tasks)} tasks created successfully",
        data=created_tasks
    )

@app.post("/api/{user_id}/tasks/bulk", response_model=BulkTaskCreateResponse)
async def create_multiple_tasks_by_user_id(user_id: str, bulk_request: BulkTaskCreateRequest):
    if user_id != MOCK_USER_ID:
        return BulkTaskCreateResponse(success=False, message="Access denied", data=[])
    
    created_tasks = []
    
    for task_create in bulk_request.tasks:
        new_task = Task(
            id=len(tasks_storage) + 1,
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id
        )
        
        tasks_storage.append(new_task)
        created_tasks.append(task_to_response(new_task))
    
    return BulkTaskCreateResponse(
        success=True,
        message=f"{len(created_tasks)} tasks created successfully",
        data=created_tasks
    )

@app.get("/api/tasks/{task_id}", response_model=SuccessResponse)
async def get_task_with_auth(task_id: int):
    task = next((task for task in tasks_storage if task.id == task_id and task.user_id == MOCK_USER_ID), None)
    
    if not task:
        return SuccessResponse(success=False, message="Task not found")
    
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

@app.get("/api/{user_id}/tasks/{task_id}", response_model=SuccessResponse)
async def get_task_by_user_id(user_id: str, task_id: int):
    if user_id != MOCK_USER_ID:
        return SuccessResponse(success=False, message="Access denied")
    
    task = next((task for task in tasks_storage if task.id == task_id and task.user_id == user_id), None)
    
    if not task:
        return SuccessResponse(success=False, message="Task not found")
    
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

@app.put("/api/tasks/{task_id}", response_model=SuccessResponse)
async def update_task_with_auth(task_id: int, task_update: TaskUpdate):
    task = next((task for task in tasks_storage if task.id == task_id and task.user_id == MOCK_USER_ID), None)
    
    if not task:
        return SuccessResponse(success=False, message="Task not found")
    
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    
    task.updated_at = datetime.now()
    
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

@app.put("/api/{user_id}/tasks/{task_id}", response_model=SuccessResponse)
async def update_task_by_user_id(user_id: str, task_id: int, task_update: TaskUpdate):
    if user_id != MOCK_USER_ID:
        return SuccessResponse(success=False, message="Access denied")
    
    task = next((task for task in tasks_storage if task.id == task_id and task.user_id == user_id), None)
    
    if not task:
        return SuccessResponse(success=False, message="Task not found")
    
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    
    task.updated_at = datetime.now()
    
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

@app.delete("/api/tasks/{task_id}", response_model=SuccessResponse)
async def delete_task_with_auth(task_id: int):
    global tasks_storage
    task_index = next((i for i, task in enumerate(tasks_storage) 
                      if task.id == task_id and task.user_id == MOCK_USER_ID), None)
    
    if task_index is None:
        return SuccessResponse(success=False, message="Task not found")
    
    tasks_storage.pop(task_index)
    
    return SuccessResponse(
        success=True,
        message="Task deleted successfully"
    )

@app.delete("/api/{user_id}/tasks/{task_id}", response_model=SuccessResponse)
async def delete_task_by_user_id(user_id: str, task_id: int):
    if user_id != MOCK_USER_ID:
        return SuccessResponse(success=False, message="Access denied")
    
    global tasks_storage
    task_index = next((i for i, task in enumerate(tasks_storage) 
                      if task.id == task_id and task.user_id == user_id), None)
    
    if task_index is None:
        return SuccessResponse(success=False, message="Task not found")
    
    tasks_storage.pop(task_index)
    
    return SuccessResponse(
        success=True,
        message="Task deleted successfully"
    )

@app.patch("/api/tasks/{task_id}/complete", response_model=SuccessResponse)
async def toggle_task_completion_with_auth(task_id: int, completion_data: TaskUpdate):
    task = next((task for task in tasks_storage if task.id == task_id and task.user_id == MOCK_USER_ID), None)
    
    if not task:
        return SuccessResponse(success=False, message="Task not found")
    
    task.completed = completion_data.completed
    task.updated_at = datetime.now()
    
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

@app.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=SuccessResponse)
async def toggle_task_completion_by_user_id(user_id: str, task_id: int, completion_data: TaskUpdate):
    if user_id != MOCK_USER_ID:
        return SuccessResponse(success=False, message="Access denied")
    
    task = next((task for task in tasks_storage if task.id == task_id and task.user_id == user_id), None)
    
    if not task:
        return SuccessResponse(success=False, message="Task not found")
    
    task.completed = completion_data.completed
    task.updated_at = datetime.now()
    
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