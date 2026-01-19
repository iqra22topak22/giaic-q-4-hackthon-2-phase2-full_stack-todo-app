from flask import Flask, request, jsonify
import json
from datetime import datetime
import uuid

app = Flask(__name__)

# Simple in-memory storage for demo purposes
tasks_storage = []

# Mock user ID for demo
MOCK_USER_ID = "demo-user-12345"

@app.route('/')
def home():
    return jsonify({"status": "Backend is running successfully (Flask Demo Mode)"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "Backend is running successfully (Flask Demo Mode)"})

# Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    user_tasks = [task for task in tasks_storage if task['user_id'] == MOCK_USER_ID]
    
    # Apply filters
    completed = request.args.get('completed')
    if completed is not None:
        completed_bool = completed.lower() == 'true'
        user_tasks = [task for task in user_tasks if task['completed'] == completed_bool]
    
    # Apply pagination
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    paginated_tasks = user_tasks[offset:offset + limit]
    
    return jsonify({
        "tasks": paginated_tasks,
        "total_count": len(user_tasks),
        "limit": limit,
        "offset": offset
    })

# Create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = {
        "id": len(tasks_storage) + 1,
        "user_id": MOCK_USER_ID,
        "title": data.get('title'),
        "description": data.get('description', ''),
        "completed": data.get('completed', False),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    tasks_storage.append(new_task)
    
    return jsonify({
        "success": True,
        "message": "Task created successfully",
        "data": new_task
    }), 201

# Bulk create tasks
@app.route('/api/tasks/bulk', methods=['POST'])
def create_tasks_bulk():
    data = request.json
    tasks_data = data.get('tasks', [])
    
    created_tasks = []
    for task_data in tasks_data:
        new_task = {
            "id": len(tasks_storage) + 1,
            "user_id": MOCK_USER_ID,
            "title": task_data.get('title'),
            "description": task_data.get('description', ''),
            "completed": task_data.get('completed', False),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        tasks_storage.append(new_task)
        created_tasks.append(new_task)
    
    return jsonify({
        "success": True,
        "message": f"{len(created_tasks)} tasks created successfully",
        "data": created_tasks
    }), 201

# Get a specific task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks_storage if task['id'] == task_id and task['user_id'] == MOCK_USER_ID), None)
    
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404
    
    return jsonify({
        "success": True,
        "data": task
    })

# Update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks_storage if task['id'] == task_id and task['user_id'] == MOCK_USER_ID), None)
    
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404
    
    data = request.json
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        "success": True,
        "message": "Task updated successfully",
        "data": task
    })

# Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks_storage
    task_index = next((i for i, task in enumerate(tasks_storage) 
                      if task['id'] == task_id and task['user_id'] == MOCK_USER_ID), None)
    
    if task_index is None:
        return jsonify({"success": False, "message": "Task not found"}), 404
    
    removed_task = tasks_storage.pop(task_index)
    
    return jsonify({
        "success": True,
        "message": "Task deleted successfully"
    })

# Toggle task completion
@app.route('/api/tasks/<int:task_id>/complete', methods=['PATCH'])
def toggle_task_completion(task_id):
    task = next((task for task in tasks_storage if task['id'] == task_id and task['user_id'] == MOCK_USER_ID), None)
    
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404
    
    data = request.json
    task['completed'] = data.get('completed', False)
    task['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        "success": True,
        "message": "Task completion status updated successfully",
        "data": task
    })

if __name__ == '__main__':
    app.run(debug=True)