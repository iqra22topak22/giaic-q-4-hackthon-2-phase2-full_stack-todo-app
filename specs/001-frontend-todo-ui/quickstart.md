# Quickstart Guide: Frontend Todo UI with Authentication

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API service

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

3. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

4. **Create environment file**
   ```bash
   cp .env.example .env.local
   ```

5. **Configure environment variables**
   Update the following in `.env.local`:
   - `NEXTAUTH_URL`: The URL where the app will be hosted
   - `NEXTAUTH_SECRET`: Secret for NextAuth (generate with `openssl rand -base64 32`)
   - `BACKEND_API_URL`: URL of the backend API service

6. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

7. **Open the application**
   Visit `http://localhost:3000` in your browser

## Key Features

### Authentication
- Navigate to `/signup` to create a new account
- Navigate to `/signin` to log in to an existing account
- Protected routes automatically redirect unauthenticated users to signin

### Task Management
- View your tasks on the dashboard at `/dashboard`
- Create new tasks using the "Add Task" button
- Edit existing tasks by clicking the edit icon
- Delete tasks using the delete button with confirmation

## API Integration
- All API calls go through the centralized API client
- JWT tokens are automatically attached to requests
- Error handling is implemented consistently across the application

## Development
- Components are organized in the `components/` directory
- API client is in `lib/api-client.ts`
- Authentication context is managed in `contexts/AuthContext.tsx`
- Type definitions are in `lib/types.ts`