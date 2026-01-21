from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import os
from datetime import datetime

# In-memory storage for tasks (will reset on each cold start)
tasks_storage = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # No database initialization needed
    print("Application started successfully")
    yield
    print("Application shutting down")

app = FastAPI(
    title="Todo API",
    description="Backend API for the Todo Web Application (Vercel Compatible)",
    version="1.0.0",
    lifespan=lifespan
)

# Get frontend origin from environment variable, with a default for development
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",  # Alternative localhost format
        "http://localhost:8000",  # Backend server (for browser requests)
        "http://127.0.0.1:8000", # Alternative localhost format
        FRONTEND_ORIGIN,  # Production frontend origin from environment variable
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers for debugging
    expose_headers=["Access-Control-Allow-Origin"]
)

# Simple in-memory models (replacing SQLModel)
class Task:
    def __init__(self, id: str, user_id: str, title: str, description: str = "", completed: bool = False, created_at: str = None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()

# Request/Response models
from pydantic import BaseModel

class TaskCreateRequest(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    completed: bool
    created_at: str

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]

@app.get("/")
def read_root():
    return {"status": "Backend is running successfully", "message": "Vercel-compatible API is accessible"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running successfully"}

# Tasks API endpoints
@app.get("/api/{user_id}/tasks", response_model=TaskListResponse)
def get_tasks(user_id: str):
    user_tasks = []
    for task_id, task in tasks_storage.items():
        if task.user_id == user_id:
            user_tasks.append(TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at
            ))
    
    return TaskListResponse(tasks=user_tasks)

@app.post("/api/{user_id}/tasks", response_model=TaskResponse)
def create_task(user_id: str, task_data: TaskCreateRequest):
    # Generate a simple ID (in production, use UUID)
    task_id = f"{user_id}_{len(tasks_storage) + 1}"
    
    new_task = Task(
        id=task_id,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )
    
    tasks_storage[task_id] = new_task
    
    return TaskResponse(
        id=new_task.id,
        user_id=new_task.user_id,
        title=new_task.title,
        description=new_task.description,
        completed=new_task.completed,
        created_at=new_task.created_at
    )

@app.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(user_id: str, task_id: str):
    task = tasks_storage.get(task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at
    )

@app.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(user_id: str, task_id: str, task_data: TaskUpdateRequest):
    task = tasks_storage.get(task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task properties if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at
    )

@app.delete("/api/{user_id}/tasks/{task_id}")
def delete_task(user_id: str, task_id: str):
    task = tasks_storage.get(task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_storage[task_id]
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))