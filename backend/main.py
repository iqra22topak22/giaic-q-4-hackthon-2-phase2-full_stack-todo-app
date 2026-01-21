from fastapi import FastAPI
from app.api.v1.tasks import router as tasks_router
from app.database import engine, create_db_and_tables
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import add_exception_handlers
from app.config import settings

load_dotenv()

# Get frontend origin from environment variable, with a default for development
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - defer any initialization to when it's actually needed
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

# Add centralized exception handlers
add_exception_handlers(app)

# Include routers
app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])

@app.get("/")
def read_root():
    return {"status": "Backend is running successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running successfully"}