# API Contract: Task Management for Todo Web Application

**Feature**: 002-backend-todo-api
**Date**: 2026-01-08
**Version**: 1.0

## Overview

This document defines the API contract for the task management functionality in the Todo Web Application backend. It specifies the endpoints, request/response formats, authentication requirements, and error handling for all task-related operations.

## Base URL

```
https://api.example.com/api/{user_id}
```

**Note**: The `{user_id}` parameter comes from the authenticated user's JWT token and should not be modified by the client.

## Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token_here>
```

The JWT token is issued by Better Auth on the frontend and must be verified by the backend using the shared secret.

## Common Response Format

Successful responses follow this structure:
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional message"
}
```

Error responses follow this structure:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## Endpoints

### 1. Get All Tasks

**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Retrieve all tasks for the authenticated user.

**Authentication**: Required - Valid JWT token

**Path Parameters**:
- `user_id` (string, required): User ID extracted from JWT token (should match token's user_id)

**Query Parameters**:
- `completed` (boolean, optional): Filter tasks by completion status
- `limit` (integer, optional): Maximum number of tasks to return (default: 50, max: 100)
- `offset` (integer, optional): Number of tasks to skip (for pagination)

**Request Headers**:
- `Authorization: Bearer <token>`

**Response Codes**:
- `200`: Success
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (attempting to access another user's tasks)
- `500`: Internal server error

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "user_id": "user123",
        "title": "Sample task",
        "description": "Task description",
        "completed": false,
        "created_at": "2023-01-01T10:00:00Z",
        "updated_at": "2023-01-01T10:00:00Z"
      }
    ],
    "total_count": 1,
    "limit": 50,
    "offset": 0
  }
}
```

### 2. Create Task

**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Create a new task for the authenticated user.

**Authentication**: Required - Valid JWT token

**Path Parameters**:
- `user_id` (string, required): User ID extracted from JWT token

**Request Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "Task title (required, 1-255 chars)",
  "description": "Task description (optional, max 1000 chars)",
  "completed": false
}
```

**Validation**:
- `title` is required and must be 1-255 characters
- `description` is optional and must be ≤ 1000 characters if provided
- `completed` is optional and defaults to `false` if not provided

**Response Codes**:
- `201`: Created successfully
- `400`: Bad request (validation error)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (attempting to create task for another user)
- `500`: Internal server error

**Success Response (201)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "New task",
    "description": "Task description",
    "completed": false,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  },
  "message": "Task created successfully"
}
```

### 3. Get Specific Task

**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Description**: Retrieve a specific task by ID for the authenticated user.

**Authentication**: Required - Valid JWT token

**Path Parameters**:
- `user_id` (string, required): User ID extracted from JWT token
- `id` (integer, required): Task ID

**Request Headers**:
- `Authorization: Bearer <token>`

**Response Codes**:
- `200`: Success
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (attempting to access another user's task)
- `404`: Not found (task doesn't exist)
- `500`: Internal server error

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  }
}
```

### 4. Update Task

**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Description**: Update an existing task for the authenticated user.

**Authentication**: Required - Valid JWT token

**Path Parameters**:
- `user_id` (string, required): User ID extracted from JWT token
- `id` (integer, required): Task ID

**Request Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "Updated task title (1-255 chars)",
  "description": "Updated task description (max 1000 chars)",
  "completed": true
}
```

**Validation**:
- `title` is optional but if provided must be 1-255 characters
- `description` is optional and must be ≤ 1000 characters if provided
- `completed` is optional (defaults to current value if not provided)

**Response Codes**:
- `200`: Updated successfully
- `400`: Bad request (validation error)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (attempting to update another user's task)
- `404`: Not found (task doesn't exist)
- `500`: Internal server error

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Updated task",
    "description": "Updated description",
    "completed": true,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-02T15:30:00Z"
  },
  "message": "Task updated successfully"
}
```

### 5. Delete Task

**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Description**: Delete a specific task by ID for the authenticated user.

**Authentication**: Required - Valid JWT token

**Path Parameters**:
- `user_id` (string, required): User ID extracted from JWT token
- `id` (integer, required): Task ID

**Request Headers**:
- `Authorization: Bearer <token>`

**Response Codes**:
- `200`: Deleted successfully
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (attempting to delete another user's task)
- `404`: Not found (task doesn't exist)
- `500`: Internal server error

**Success Response (200)**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### 6. Toggle Task Completion

**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Description**: Toggle the completion status of a specific task for the authenticated user.

**Authentication**: Required - Valid JWT token

**Path Parameters**:
- `user_id` (string, required): User ID extracted from JWT token
- `id` (integer, required): Task ID

**Request Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "completed": true
}
```

**Alternative**: Empty body to simply toggle the current status

**Response Codes**:
- `200`: Updated successfully
- `400`: Bad request (invalid request body)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (attempting to update another user's task)
- `404`: Not found (task doesn't exist)
- `500`: Internal server error

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Sample task",
    "description": "Task description",
    "completed": true,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-02T15:30:00Z"
  },
  "message": "Task completion status updated successfully"
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `AUTH_INVALID_TOKEN` | 401 | Provided JWT token is invalid |
| `AUTH_EXPIRED_TOKEN` | 401 | Provided JWT token has expired |
| `AUTH_MISSING_TOKEN` | 401 | No JWT token provided in request |
| `ACCESS_DENIED` | 403 | Attempting to access resources owned by another user |
| `VALIDATION_ERROR` | 422 | Request body validation failed |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource does not exist |
| `INTERNAL_ERROR` | 500 | An unexpected error occurred on the server |

## Security Considerations

1. **User Isolation**: The `user_id` in the URL path must match the `user_id` in the JWT token. The system must validate this match to prevent cross-user data access.

2. **Token Validation**: All requests must validate the JWT token using the Better Auth shared secret.

3. **Input Sanitization**: All inputs must be validated and sanitized to prevent injection attacks.

4. **Rate Limiting**: Implement rate limiting to prevent abuse of the API.

## Versioning

This API contract follows semantic versioning. Breaking changes will result in a major version increment. Minor version increments will include backwards-compatible additions.

## Client Implementation Guidelines

1. Always include the JWT token in the Authorization header for authenticated requests
2. Handle all documented error responses appropriately
3. Respect rate limits and implement exponential backoff if needed
4. Validate response schemas before processing data
5. Use the `user_id` from the JWT token, never from other sources