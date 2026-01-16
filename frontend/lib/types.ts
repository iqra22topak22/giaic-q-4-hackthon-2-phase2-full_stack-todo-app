// User Session entity
export interface UserSession {
  userId: string;
  token: string;
  expiresAt: Date;
  isAuthenticated: boolean;
}

// Task entity
export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'completed';
  createdAt: Date;
  updatedAt: Date;
  userId: string;
}

// Authentication Form entity
export interface AuthenticationForm {
  email: string;
  password: string;
  confirmPassword?: string;
}

// Task Form entity
export interface TaskForm {
  title: string;
  description?: string;
  status: 'pending' | 'completed';
}

// API Response structure
export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
}

// Authentication response
export interface AuthResponse {
  success: boolean;
  message: string;
  token?: string;
  user?: {
    id: string;
    email: string;
  };
}