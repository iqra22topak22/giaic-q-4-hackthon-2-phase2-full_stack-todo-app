# api/index.py
import asyncio
import os
import sys
from typing import Dict, Any

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from mangum import Mangum

# Create the Mangum adapter for AWS Lambda compatibility
handler = Mangum(app)

# Define the async function that Vercel will call
async def main(event: Dict[str, Any], context: Any):
    # This is called by Vercel's Python runtime
    return await handler(event, context)