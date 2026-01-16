# Todo App - Development Setup Guide

## Backend (FastAPI)

### Starting the Backend Server

To start the backend server in development mode:

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Or use the development script:

```bash
cd backend
python dev_server.py
```

### Backend Features in Development Mode

- CORS is configured to allow requests from `http://localhost:3000`
- Authentication is bypassed using a default `dev-user-id`
- In-memory storage is used instead of database
- All API endpoints are accessible at `http://127.0.0.1:8000`

### API Endpoints

The backend provides the following endpoints:

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a specific task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Frontend (Next.js)

### Starting the Frontend Server

To start the frontend server:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Frontend API Routes

The frontend provides proxy API routes that forward requests to the backend:

- `GET /api/tasks?userId={userId}` - Gets tasks via proxy
- `POST /api/tasks?userId={userId}` - Creates task via proxy
- `GET /api/tasks/[id]?userId={userId}` - Gets specific task via proxy
- `PUT /api/tasks/[id]?userId={userId}` - Updates specific task via proxy
- `DELETE /api/tasks/[id]?userId={userId}` - Deletes specific task via proxy

### Direct Backend Requests

You can also make direct requests to the backend from frontend components:

```javascript
// Example of direct request to backend
const response = await fetch('http://127.0.0.1:8000/api/dev-user-id/tasks', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
});
```

## Development Notes

1. The backend runs on port 8000
2. The frontend runs on port 3000
3. CORS is configured to allow communication between the two
4. In development, use `dev-user-id` as the userId
5. The backend uses in-memory storage in development mode
6. Both servers should be running simultaneously for full functionality

## Troubleshooting

If you encounter timeout errors:
1. Ensure both servers are running
2. Check that the backend is accessible at http://127.0.0.1:8000
3. Verify that the frontend is making requests with the correct userId
4. Check the browser console and server logs for error messages