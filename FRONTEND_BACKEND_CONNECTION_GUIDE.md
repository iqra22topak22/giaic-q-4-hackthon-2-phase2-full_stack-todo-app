# Connecting Frontend to Deployed Backend

This guide explains how to connect your deployed frontend (on Vercel) with your deployed backend (also on Vercel).

## Step 1: Get Your Backend URL

After deploying your backend to Vercel, you'll have a URL in this format:
```
https://your-backend-project-name.vercel.app
```

## Step 2: Configure Environment Variable in Frontend

1. Go to your frontend project in the Vercel dashboard
2. Navigate to Settings > Environment Variables
3. Add a new environment variable:
   - Key: `NEXT_PUBLIC_BACKEND_API_URL`
   - Value: Your deployed backend URL (e.g., `https://your-backend-project-name.vercel.app`)
4. Save the changes

## Step 3: Update CORS Settings in Backend

Make sure your backend accepts requests from your frontend domain:

1. In your backend's `main.py` file, update the CORS settings:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:3000",  # Next.js development server
           "http://127.0.0.1:3000",  # Alternative localhost format
           "http://localhost:8000",  # Backend server (for browser requests)
           "http://127.0.0.1:8000", # Alternative localhost format
           "https://your-frontend-domain.vercel.app",  # Your deployed frontend
           # Add your custom domain if you have one
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
       expose_headers=["Access-Control-Allow-Origin"]
   )
   ```

2. Re-deploy your backend with the updated CORS settings

## Step 4: Redeploy Frontend

After adding the environment variable, redeploy your frontend for the changes to take effect:
1. Push an update to your GitHub repository, or
2. Use the Vercel CLI: `vercel --prod`

## Step 5: Test the Connection

1. Visit your deployed frontend
2. Log in to your account
3. Try creating, updating, and deleting tasks
4. Verify that all API calls are working correctly

## Troubleshooting

If you encounter issues:

1. **CORS errors**: Make sure your backend's CORS settings include your frontend's domain
2. **Network errors**: Verify that your `NEXT_PUBLIC_BACKEND_API_URL` is set correctly
3. **Authentication errors**: Ensure JWT tokens are being properly sent with requests
4. **API endpoint errors**: Check that your API routes match between frontend and backend

## Additional Notes

- The frontend uses the `NEXT_PUBLIC_BACKEND_API_URL` environment variable to determine where to send API requests
- All API calls in the frontend automatically include the user ID from localStorage in the URL
- Authentication tokens are automatically attached to requests when available