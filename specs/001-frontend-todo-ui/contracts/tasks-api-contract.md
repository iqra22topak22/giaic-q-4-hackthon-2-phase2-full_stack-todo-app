# API Contracts: Frontend Todo UI with Authentication

## Authentication Endpoints

### POST /api/auth/signup
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "confirmPassword": "securePassword123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Account created successfully",
  "user": {
    "id": "user_12345",
    "email": "user@example.com"
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Email already exists"
}
```

### POST /api/auth/signin
Authenticate a user and return session information.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Sign in successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

### POST /api/auth/signout
End the current user session.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "success": true,
  "message": "Signed out successfully"
}
```

## Task Management Endpoints

### GET /api/tasks
Retrieve all tasks for the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (Success):**
```json
{
  "success": true,
  "data": [
    {
      "id": "task_123",
      "title": "Sample Task",
      "description": "Sample task description",
      "status": "pending",
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z",
      "userId": "user_12345"
    }
  ]
}
```

### POST /api/tasks
Create a new task for the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "status": "pending"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Task created successfully",
  "data": {
    "id": "task_456",
    "title": "New Task",
    "description": "Task description",
    "status": "pending",
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:00Z",
    "userId": "user_12345"
  }
}
```

### PUT /api/tasks/{taskId}
Update an existing task.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request Body:**
```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "status": "completed"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Task updated successfully",
  "data": {
    "id": "task_123",
    "title": "Updated Task",
    "description": "Updated description",
    "status": "completed",
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-02T00:00:00Z",
    "userId": "user_12345"
  }
}
```

### DELETE /api/tasks/{taskId}
Delete a task.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Response (Error - Unauthorized):**
```json
{
  "success": false,
  "message": "Unauthorized"
}
```

**Response (Error - Not Found):**
```json
{
  "success": false,
  "message": "Task not found"
}
```