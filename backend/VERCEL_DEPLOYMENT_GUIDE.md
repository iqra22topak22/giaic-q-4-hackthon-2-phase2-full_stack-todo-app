# Deploying Backend to Vercel

Follow these steps to deploy your FastAPI backend to Vercel:

## Prerequisites

1. Sign up for a Vercel account at https://vercel.com/
2. Install the Vercel CLI globally:
   ```bash
   npm install -g vercel
   ```

## Steps to Deploy

1. Navigate to your backend directory:
   ```bash
   cd C:\Users\pc\Desktop\full_stack_todo\backend
   ```

2. Login to Vercel (optional but recommended):
   ```bash
   vercel login
   ```

3. Initialize your project on Vercel:
   ```bash
   vercel
   ```

4. During the setup:
   - Set the Root Directory to your backend folder
   - When prompted for the build command, press Enter to use the default
   - When prompted for the output directory, press Enter to use the default
   - For the framework, select "Other" or "Python" if available

5. Set Environment Variables:
   - Go to your project dashboard on Vercel
   - Navigate to Settings > Environment Variables
   - Add the following variables:
     - `ENV`: `production`
     - `DATABASE_URL`: Use a production database URL (PostgreSQL recommended)
     - `SECRET_KEY`: A strong secret key for JWT signing

6. Redeploy after setting environment variables:
   ```bash
   vercel --prod
   ```

## Alternative Method: Git Integration

1. Push your code to GitHub (which you already have at https://github.com/iqra22topak22/giaic-q-4-hackthon-2-phase2-full_stack-todo-app)
2. Go to https://vercel.com/dashboard
3. Click "Add New..." and select "Project"
4. Import your GitHub repository
5. Select your backend directory
6. Set the build command to `pip install -r requirements.txt && python -c "import main"`
7. Set the output directory if needed
8. Add the environment variables as mentioned above
9. Click "Deploy"

## Important Notes

- The deployed backend will use SQLite in production mode, which is not ideal for production. Consider switching to PostgreSQL for production.
- Update the CORS settings in main.py to reflect your actual frontend domain after deployment.
- Make sure to set a strong SECRET_KEY in your environment variables.
- The current setup uses an in-memory database in development but will switch to SQLite in production.

## Verifying Deployment

Once deployed, visit the provided URL to check:
- `/` - Health check endpoint
- `/docs` - Interactive API documentation
- `/redoc` - Alternative API documentation