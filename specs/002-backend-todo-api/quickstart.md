# Quickstart Guide: Backend API for Todo Web Application

**Feature**: 002-backend-todo-api
**Date**: 2026-01-08

## Overview

This guide provides a quick setup and run procedure for the Todo Web Application backend service. It covers environment setup, dependency installation, configuration, and initial run instructions.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Access to Neon Serverless PostgreSQL database
- Better Auth shared secret for JWT verification

## Setup Instructions

### 1. Clone or Navigate to Project Directory

```bash
cd path/to/hacthone_2p2/phase_2
```

### 2. Create Virtual Environment

```bash
python -m venv backend-env
```

### 3. Activate Virtual Environment

On Windows:
```bash
backend-env\Scripts\activate
```

On macOS/Linux:
```bash
source backend-env/bin/activate
```

### 4. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

If requirements.txt doesn't exist yet, install the core dependencies:

```bash
pip install fastapi uvicorn sqlmodel pyjwt python-multipart psycopg2-binary python-dotenv
```

### 5. Environment Configuration

Create a `.env` file in the backend root directory with the following variables:

```env
DATABASE_URL=postgresql+psycopg2://username:password@host:port/database_name
BETTER_AUTH_SECRET=your_better_auth_shared_secret
BETTER_AUTH_URL=https://your-app.better-auth.com
ENVIRONMENT=development  # or production
```

### 6. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuration and environment variables
│   ├── database.py         # Database connection and session management
│   ├── auth.py             # JWT authentication utilities
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py         # Task model definition
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py         # Pydantic schemas for validation
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── tasks.py    # Task-related API endpoints
│   └── utils/
│       ├── __init__.py
│       └── validators.py   # Validation utilities
└── tests/
    ├── __init__.py
    ├── conftest.py         # Test configuration
    └── test_tasks.py       # Task API tests
```

## API Endpoints

Once running, the following endpoints will be available:

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Testing the API

### Using curl

First, obtain a valid JWT token from your Better Auth implementation, then:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/user123/tasks
```

### Using Python requests

```python
import requests

headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
}

response = requests.get("http://localhost:8000/api/user123/tasks", headers=headers)
print(response.json())
```

## Running Tests

```bash
pytest tests/
```

Or for verbose output:

```bash
pytest tests/ -v
```

## Configuration Options

- `ENVIRONMENT`: Set to "production" for production mode, "development" for development
- `DATABASE_URL`: Connection string for the PostgreSQL database
- `BETTER_AUTH_SECRET`: Shared secret for JWT verification
- `BETTER_AUTH_URL`: URL of the Better Auth instance

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure your virtual environment is activated and dependencies are installed
2. **Database Connection Error**: Verify your DATABASE_URL is correct and the database is accessible
3. **JWT Validation Error**: Ensure the BETTER_AUTH_SECRET matches the one used by your Better Auth instance

### Enable Debug Mode

Add `DEBUG=true` to your `.env` file to enable more detailed error messages during development.

## Next Steps

1. Implement the models as defined in the data-model.md
2. Create the API endpoints following the contracts in the API contract document
3. Implement authentication utilities
4. Add comprehensive tests
5. Deploy to your preferred hosting platform