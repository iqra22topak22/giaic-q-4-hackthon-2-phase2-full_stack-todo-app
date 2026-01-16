from typing import Dict, List, Optional
from app.models.task import Task
from datetime import datetime
import uuid

# In-memory storage for tasks
# Initialize with default dev users for development
tasks_db: Dict[str, List[Task]] = {
    "dev-user-id": [],  # Default dev user with empty task list
    "mock-user-id": []  # Mock user for development
}

def get_tasks_for_user(user_id: str) -> List[Task]:
    """Get all tasks for a specific user."""
    return tasks_db.get(user_id, [])

def add_task_for_user(user_id: str, task: Task) -> Task:
    """Add a task for a specific user."""
    if user_id not in tasks_db:
        tasks_db[user_id] = []

    # Assign a unique ID to the task
    if not task.id:
        # Find the next available ID
        existing_ids = [t.id for t in tasks_db[user_id] if t.id]
        task.id = max(existing_ids) + 1 if existing_ids else 1
    else:
        # Check if ID already exists and increment if needed
        existing_ids = [t.id for t in tasks_db[user_id] if t.id]
        if task.id in existing_ids:
            # Find the highest ID and assign the next one
            task.id = max(existing_ids) + 1 if existing_ids else 1

    task.created_at = task.created_at or datetime.utcnow()
    task.updated_at = task.updated_at or datetime.utcnow()

    tasks_db[user_id].append(task)
    return task

def get_task_for_user(user_id: str, task_id: int) -> Optional[Task]:
    """Get a specific task for a user by ID."""
    user_tasks = tasks_db.get(user_id, [])
    for task in user_tasks:
        if task.id == task_id:
            return task
    return None

def update_task_for_user(user_id: str, task_id: int, updated_task: Task) -> Optional[Task]:
    """Update a specific task for a user."""
    user_tasks = tasks_db.get(user_id, [])
    for i, task in enumerate(user_tasks):
        if task.id == task_id:
            # Preserve the original creation time
            updated_task.created_at = task.created_at
            updated_task.updated_at = datetime.utcnow()
            updated_task.id = task_id  # Ensure ID doesn't change
            user_tasks[i] = updated_task
            return updated_task
    return None

def delete_task_for_user(user_id: str, task_id: int) -> bool:
    """Delete a specific task for a user."""
    user_tasks = tasks_db.get(user_id, [])
    for i, task in enumerate(user_tasks):
        if task.id == task_id:
            del user_tasks[i]
            return True
    return False