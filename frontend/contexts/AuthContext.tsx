// frontend/contexts/AuthContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { UserSession } from '../lib/types';
import { jwtDecode } from 'jwt-decode';

interface AuthContextType {
  userSession: UserSession | null;
  login: (token: string, userId?: string) => void;
  logout: () => void;
  signup: (email: string, password: string) => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [userSession, setUserSession] = useState<UserSession | null>(null);

  useEffect(() => {
    // Check if user is already logged in on initial load
    const token = localStorage.getItem('jwt_token');

    if (token) {
      try {
        // Decode the JWT to get the user ID
        const decodedToken: any = jwtDecode(token);
        const userId = decodedToken.sub; // 'sub' is the subject claim, usually the user ID

        const session: UserSession = {
          userId,
          token,
          expiresAt: new Date(decodedToken.exp * 1000), // Convert Unix timestamp to JS Date
          isAuthenticated: true,
        };
        setUserSession(session);
      } catch (error) {
        console.error('Error decoding token:', error);
        // If there's an error decoding the token, clear it
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('token_expires_at');
      }
    }
  }, []);

  const login = (token: string, userId?: string) => {
    try {
      // Decode the JWT to get the user ID if not provided
      let actualUserId = userId;
      if (!actualUserId) {
        const decodedToken: any = jwtDecode(token);
        actualUserId = decodedToken.sub; // 'sub' is the subject claim, usually the user ID
      }

      // Get expiration time from the token
      const decodedToken: any = jwtDecode(token);
      const expiresAt = new Date(decodedToken.exp * 1000); // Convert Unix timestamp to JS Date

      const session: UserSession = {
        userId: actualUserId,
        token,
        expiresAt,
        isAuthenticated: true,
      };

      // Store in localStorage
      localStorage.setItem('jwt_token', token);
      localStorage.setItem('user_id', actualUserId);
      localStorage.setItem('token_expires_at', expiresAt.toISOString());

      setUserSession(session);
    } catch (error) {
      console.error('Error during login:', error);
      throw new Error('Invalid token');
    }
  };

  const logout = () => {
    // Clear from localStorage
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('token_expires_at');

    setUserSession({
      userId: '',
      token: '',
      expiresAt: new Date(),
      isAuthenticated: false,
    });
  };

  const signup = async (email: string, password: string): Promise<boolean> => {
    try {
      // This would typically call an API endpoint
      // For now, we'll just return true to simulate success
      return true;
    } catch (error) {
      console.error('Signup error:', error);
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ userSession, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};