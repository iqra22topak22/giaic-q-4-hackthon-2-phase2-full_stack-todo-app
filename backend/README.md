# Todo Web Application Backend API

This is the backend API for the Todo Web Application, built with FastAPI and SQLModel.

## Features

- JWT-based authentication using Better Auth
- Secure CRUD operations for user tasks
- User-based data isolation
- RESTful API design
- Input validation and error handling

## API Endpoints

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```
   DATABASE_URL=postgresql+psycopg2://username:password@host:port/database_name
   BETTER_AUTH_SECRET=your_better_auth_shared_secret
   BETTER_AUTH_URL=https://your-app.better-auth.com
   ENVIRONMENT=development
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Testing

Run the tests using pytest:
```bash
pytest tests/
```