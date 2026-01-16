"""
Development startup script for the Todo API
This script ensures the backend is properly configured for development
"""

import uvicorn
from app.config import settings

def main():
    print(f"Starting Todo API in {settings.ENVIRONMENT} mode...")
    print("Backend will be available at: http://127.0.0.1:8000")
    print("CORS is configured to allow requests from: http://localhost:3000")
    print("Using in-memory storage for development...")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["."],
        log_level="info"
    )

if __name__ == "__main__":
    main()