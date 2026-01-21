from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from fastapi.middleware.cors import CORSMiddleware

# Get frontend origin from environment variable, with a default for development
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Minimal lifespan - no database initialization
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="Todo API",
    description="Backend API for the Todo Web Application",
    version="1.0.0",
    lifespan=lifespan
)

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

@app.get("/")
def read_root():
    return {"status": "Backend is running successfully", "message": "API is accessible"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running successfully"}

# Placeholder for task routes - would normally be imported from the router
@app.get("/api/{user_id}/tasks")
def get_tasks(user_id: str):
    return {"user_id": user_id, "tasks": [], "message": "Tasks endpoint is accessible but database is not configured for this deployment"}

@app.post("/api/{user_id}/tasks")
def create_task(user_id: str):
    return {"user_id": user_id, "task": None, "message": "Create task endpoint is accessible but database is not configured for this deployment"}