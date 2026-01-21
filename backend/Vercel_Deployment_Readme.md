# Backend Deployment Guide for Vercel

## Current Status
The backend has been deployed to: https://backend-virid-phi-36.vercel.app

## Known Issues
Currently, the deployment has issues with database initialization on Vercel's serverless functions due to the ephemeral nature of the file system. SQLite databases don't work well in Vercel's environment.

## Recommended Solution
For a production-ready deployment, you should:

1. Set up a PostgreSQL database (e.g., using Neon, Supabase, or AWS RDS)
2. Add the database URL as an environment variable in Vercel:
   - Key: `DATABASE_URL`
   - Value: Your PostgreSQL connection string

## Environment Variables Required
- `DATABASE_URL`: PostgreSQL database URL (e.g., postgresql://user:password@host:port/database)
- `SECRET_KEY`: Secret key for JWT tokens
- `ENVIRONMENT`: Set to "production"

## Local Development
For local development, the application will continue to use SQLite as configured.

## API Endpoints
- `/` - Health check
- `/health` - Detailed health check
- `/docs` - API Documentation (Swagger UI)
- `/redoc` - API Documentation (ReDoc)
- `/api/{user_id}/tasks` - Task management endpoints