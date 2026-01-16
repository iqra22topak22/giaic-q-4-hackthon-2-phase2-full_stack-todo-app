// frontend/components/Providers.tsx
'use client';

import React, { ReactNode } from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import { ToastProvider } from '../contexts/ToastContext';
import AppErrorBoundary from './error/AppErrorBoundary';

interface ProvidersProps {
  children: ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
  return (
    <AuthProvider>
      <ToastProvider>
        <AppErrorBoundary>
          {children}
        </AppErrorBoundary>
      </ToastProvider>
    </AuthProvider>
  );
}