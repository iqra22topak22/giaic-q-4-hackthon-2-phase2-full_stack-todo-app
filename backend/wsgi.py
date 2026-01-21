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
# This version uses in-memory storage to avoid database issues on Vercel
from vercel_compatible_main import app

# For Vercel Python runtime
application = app