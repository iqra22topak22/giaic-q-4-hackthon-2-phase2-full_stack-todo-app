from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.user_auth.router import router as auth_router
from app.tasks.router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_db_and_tables()
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
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],  # Allow Next.js frontend
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