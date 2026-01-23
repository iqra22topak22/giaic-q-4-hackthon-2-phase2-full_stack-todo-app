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
   # For local development with SQLite:
   DATABASE_URL=sqlite+aiosqlite:///./todo_app.db

   # For production with Neon PostgreSQL, use your actual connection string:
   # DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx-neon-project-name.region.provider.neon.tech/dbname

   BETTER_AUTH_SECRET=your_better_auth_shared_secret
   BETTER_AUTH_URL=https://your-app.better-auth.com
   ENVIRONMENT=development
   ```

## Configuring Neon PostgreSQL

To use Neon as your database:

1. Create a Neon account at [neon.tech](https://neon.tech)
2. Create a new project in Neon
3. Copy your connection string from the Neon dashboard
4. Update your `.env` file with the actual connection string:
   ```
   DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx-neon-project-name.region.provider.neon.tech/dbname
   ```
5. Make sure to install the required dependencies:
   ```bash
   pip install asyncpg
   ```

## Setup (continued)

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Testing

Run the tests using pytest:
```bash
pytest tests/
```