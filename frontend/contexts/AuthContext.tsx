// frontend/contexts/AuthContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { UserSession } from '../lib/types';

interface AuthContextType {
  userSession: UserSession | null;
  login: (token: string, userId: string) => void;
  logout: () => void;
  signup: (email: string, password: string) => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [userSession, setUserSession] = useState<UserSession | null>(null);

  useEffect(() => {
    // Check if user is already logged in on initial load
    const token = localStorage.getItem('jwt_token');
    const userId = localStorage.getItem('user_id');

    if (token && userId) {
      const session: UserSession = {
        userId,
        token,
        expiresAt: new Date(localStorage.getItem('token_expires_at') || Date.now()),
        isAuthenticated: true,
      };
      setUserSession(session);
    }
  }, []);

  const login = (token: string, userId: string) => {
    // Calculate expiration time (assuming token is valid for 24 hours)
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 1); // 24 hours from now

    const session: UserSession = {
      userId,
      token,
      expiresAt,
      isAuthenticated: true,
    };

    // Store in localStorage
    localStorage.setItem('jwt_token', token);
    localStorage.setItem('user_id', userId);
    localStorage.setItem('token_expires_at', expiresAt.toISOString());

    setUserSession(session);
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