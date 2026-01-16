// frontend/components/auth/ProtectedRoute.tsx
import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { userSession } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If user is not authenticated, redirect to signin
    if (!userSession?.isAuthenticated) {
      router.push('/signin');
    }
  }, [userSession, router]);

  // If not authenticated, don't render anything (redirect will happen)
  if (!userSession?.isAuthenticated) {
    return <div>Redirecting...</div>;
  }

  // If authenticated, render the protected content
  return <>{children}</>;
};

export default ProtectedRoute;