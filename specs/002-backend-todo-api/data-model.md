# Data Model: Backend API for Todo Web Application

**Feature**: 002-backend-todo-api
**Date**: 2026-01-08

## Overview

This document defines the data model for the Todo Web Application backend, specifying the structure of data entities, their relationships, validation rules, and state transitions.

## Entity Definitions

### Task

**Description**: Represents a user's task with attributes for tracking and management.

**Fields**:
- `id` (Integer, Primary Key, Auto-generated)
  - Unique identifier for the task
  - Auto-incremented integer value
- `user_id` (String, Foreign Key)
  - References the user who owns this task
  - Extracted from JWT token, never from request body
  - Used for enforcing data isolation between users
- `title` (String, Required)
  - Title of the task
  - Length: minimum 1 character, maximum 255 characters
- `description` (String, Optional)
  - Detailed description of the task
  - Length: maximum 1000 characters
- `completed` (Boolean)
  - Status of the task completion
  - Default value: `false`
- `created_at` (DateTime, Timestamp)
  - Timestamp when the task was created
  - Automatically set when record is created
  - Format: ISO 8601 datetime string
- `updated_at` (DateTime, Timestamp)
  - Timestamp when the task was last updated
  - Automatically updated when record is modified
  - Format: ISO 8601 datetime string

**Relationships**:
- Belongs to one User (via user_id foreign key)
- User can have many Tasks

**Validation Rules**:
- `title` must be between 1 and 255 characters
- `description` must be 1000 characters or less (if provided)
- `completed` must be a boolean value
- `user_id` must match the authenticated user's ID from JWT token
- `created_at` and `updated_at` are automatically managed by the system

**State Transitions**:
- `completed` field can transition from `false` to `true` or vice versa
- All other fields can be modified except `id` and `user_id`

### User (External Reference)

**Description**: Represents a user of the system, with user_id extracted from security token (managed externally by authentication system).

**Fields**:
- `user_id` (String, Primary Identifier)
  - Unique identifier for the user
  - Extracted from JWT token
  - Used as foreign key in Task entity

**Relationships**:
- Has many Tasks
- Authentication and user management handled externally by Better Auth

## Database Schema

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for efficient user-based queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for efficient completion status queries
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## Data Access Patterns

### Query Patterns
1. **Get all tasks for a user**: Filter by `user_id`
2. **Get specific task**: Filter by `user_id` and `id`
3. **Filter completed tasks**: Filter by `user_id` and `completed`
4. **Search tasks by title**: Filter by `user_id` and partial title match

### Security Constraints
- All queries must include `user_id` filter to enforce data isolation
- No cross-user data access is allowed
- `user_id` must always come from authenticated JWT token, never from request payload

## Data Lifecycle

### Creation
- When a new task is created:
  - `id` is auto-generated
  - `user_id` is extracted from JWT token
  - `title` is validated for length requirements
  - `completed` defaults to `false`
  - `created_at` and `updated_at` are set to current timestamp

### Updates
- When a task is updated:
  - `updated_at` is automatically set to current timestamp
  - `user_id` cannot be changed
  - Validation rules are applied to updated fields

### Deletion
- When a task is deleted:
  - Only the owner (authenticated user) can delete their tasks
  - Soft delete could be implemented with a `deleted_at` field if needed

## Business Rules

1. **Ownership Enforcement**: Users can only access, modify, or delete their own tasks
2. **Data Integrity**: All validation rules must pass before saving to database
3. **Timestamp Management**: `created_at` and `updated_at` are managed automatically
4. **Title Requirements**: Task titles must be between 1 and 255 characters
5. **Description Limits**: Descriptions must be 1000 characters or less