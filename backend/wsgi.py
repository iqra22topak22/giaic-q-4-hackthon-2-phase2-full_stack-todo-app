import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variable for production
os.environ.setdefault('ENV', 'production')

# Import and serve the FastAPI app
from main import app

# Vercel expects the application to be named 'app'
application = app