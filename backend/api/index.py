import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment to production
os.environ.setdefault('ENVIRONMENT', 'production')
os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///:memory:')  # Use in-memory DB for Vercel

# Import the FastAPI app from our simple test version
from simple_test_main import app

# Vercel expects the application to be named 'app'
# This is the entry point for Vercel's Python runtime
handler = app