import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment to production
os.environ.setdefault('ENVIRONMENT', 'production')
os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///:memory:')  # Use in-memory DB for Vercel

# Import required modules first
import asyncio

# Import the app from vercel_compatible_main (our new Vercel-friendly version)
try:
    from vercel_compatible_main import app
except ImportError as e:
    # If vercel_compatible_main import fails, fall back to minimal_main, then main
    try:
        from minimal_main import app
    except ImportError:
        from main import app

# For Vercel Python runtime
application = app