from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.user_auth.router import router as auth_router
from app.tasks.router import router as tasks_router

app = FastAPI(
    title="Todo API",
    description="Backend API for the Todo Web Application",
    version="1.0.0"
)

import os

# Configure CORS middleware
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "https://full-stack-todo-iqra22topak22s-projects.vercel.app",  # Production Vercel URL
    "https://full-stack-todo-cxdbrdr8s-iqra22topak22s-projects.vercel.app",  # Latest deployment
    "https://full-stack-todo-eta.vercel.app",  # Main alias
    "https://full-stack-todo-qfzzohhhm-iqra22topak22s-projects.vercel.app",  # Current deployment
    "https://full-stack-todo-pqznvemgs-iqra22topak22s-projects.vercel.app"  # Current deployment
]

# Add any additional origins from environment variables
cors_env_var = os.getenv("CORS_ALLOWED_ORIGINS") or os.getenv("ALLOWED_ORIGINS")
if cors_env_var:
    origins_list = [origin.strip() for origin in cors_env_var.split(",") if origin.strip()]
    allowed_origins.extend(origins_list)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(tasks_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "Backend is running successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running successfully"}

# For Vercel deployment, we don't initialize the database on startup
# as it's a serverless environment