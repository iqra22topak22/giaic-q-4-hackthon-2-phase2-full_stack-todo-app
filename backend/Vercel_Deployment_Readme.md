# Backend Deployment Guide for Vercel

## Current Status
The backend has been deployed to: https://backend-virid-phi-36.vercel.app

## Known Issues
Currently, the deployment has issues with database initialization on Vercel's serverless functions due to the ephemeral nature of the file system. SQLite databases don't work well in Vercel's environment, resulting in FUNCTION_INVOCATION_FAILED errors.

## Recommended Solution
For a production-ready deployment, you must:

1. Set up a PostgreSQL database (e.g., using Neon, Supabase, or AWS RDS)
2. Add the database URL as an environment variable in Vercel:
   - Key: `DATABASE_URL`
   - Value: Your PostgreSQL connection string
3. Additionally, set these environment variables in your Vercel project:
   - `SECRET_KEY`: A strong secret key for JWT tokens
   - `ENVIRONMENT`: Set to "production"

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

## Important Note
Until you configure a proper PostgreSQL database and set the environment variables in your Vercel project, the backend will continue to show 500 errors. The frontend has been deployed and is working correctly, but it will not be able to communicate with the backend until these changes are made.

## Steps to Fix Backend 500 Error
1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Navigate to your backend project
3. Go to Settings > Environment Variables
4. Add the following variables:
   - `DATABASE_URL`: PostgreSQL database URL (e.g., postgresql://user:password@host:port/database)
   - `SECRET_KEY`: A strong secret key for JWT tokens
   - `ENVIRONMENT`: production
5. Redeploy your project after adding these variables