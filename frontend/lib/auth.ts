// frontend/lib/auth.ts
// This file contains authentication-related utility functions

// Helper function to safely access localStorage
const getLocalStorage = (): Storage | null => {
  if (typeof window !== 'undefined') {
    return window.localStorage;
  }
  return null;
};

// Function to sign out the user
export const signOut = (): void => {
  const storage = getLocalStorage();
  if (storage) {
    // Remove the JWT token from localStorage
    storage.removeItem('jwt_token');
    storage.removeItem('user_id');
    storage.removeItem('token_expires_at');
  }

  // Redirect to the login page
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
};

// Function to check if the user is authenticated
export const isAuthenticated = (): boolean => {
  const storage = getLocalStorage();
  if (!storage) return false;

  const token = storage.getItem('jwt_token');
  const userId = storage.getItem('user_id');

  // In development, allow mock-user-id without token
  if (process.env.NODE_ENV === 'development' && userId && userId === 'mock-user-id') {
    return true;
  }

  // Check if both token and userId exist
  if (!token || !userId) {
    return false;
  }

  // Check if the token has expired
  const expiresAt = storage.getItem('token_expires_at');
  if (expiresAt) {
    const expirationDate = new Date(expiresAt);
    if (expirationDate < new Date()) {
      // Token has expired, remove it
      storage.removeItem('jwt_token');
      storage.removeItem('user_id');
      storage.removeItem('token_expires_at');
      return false;
    }
  }

  return true;
};

// Function to get the current user's token
export const getCurrentToken = (): string | null => {
  const storage = getLocalStorage();
  if (!storage) return null;

  // In development, return null for mock-user-id
  if (process.env.NODE_ENV === 'development') {
    const userId = storage.getItem('user_id');
    if (userId && userId === 'mock-user-id') {
      return null;
    }
  }

  return storage.getItem('jwt_token');
};

// Function to get the current user's ID
export const getCurrentUserId = (): string | null => {
  const storage = getLocalStorage();
  if (!storage) return null;

  return storage.getItem('user_id');
};

// Function to set the mock user ID in development
export const setMockUserId = (userId: string): void => {
  const storage = getLocalStorage();
  if (!storage) return;

  if (process.env.NODE_ENV === 'development') {
    storage.setItem('user_id', userId);
    // Also clear any existing token since mock users don't need tokens
    storage.removeItem('jwt_token');
    storage.removeItem('token_expires_at');
  }
};