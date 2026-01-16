import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { isAuthenticated } from '../lib/auth';

interface AuthGuardProps {
  children: React.ReactNode;
}

const AuthGuard: React.FC<AuthGuardProps> = ({ children }) => {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      // Redirect to login if not authenticated
      router.push('/login');
    }
  }, [router]);

  // If not authenticated, don't render children
  if (!isAuthenticated()) {
    return null; // Render nothing while redirecting
  }

  return <>{children}</>;
};

export default AuthGuard;