from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started successfully")
    yield
    print("Application shutting down")

app = FastAPI(
    title="Simple Test API",
    description="Simple API for testing",
    version="1.0.0",
    lifespan=lifespan
)

# Get frontend origin from environment variable, with a default for development
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

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
)

@app.get("/")
def read_root():
    return {"status": "Backend is running successfully", "message": "Simple test API is working"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Simple test API is working"}