import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { isAuthenticated } from '../lib/auth';
import { ThemeProvider } from '../contexts/theme-context';
import { AuthProvider } from '../contexts/AuthContext';

// Pages that don't require authentication
const publicPages = ['/', '/login', '/signup'];

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter();

  useEffect(() => {
    // Check authentication for protected routes
    const checkAuth = () => {
      if (!publicPages.includes(router.pathname) && !isAuthenticated()) {
        // Redirect to login if not authenticated and trying to access protected route
        router.push('/login');
      }
    };

    // Run check on initial load
    checkAuth();

    // Listen for route changes
    const handleRouteChange = () => {
      checkAuth();
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    // Cleanup listener on unmount
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);

  return (
    <AuthProvider>
      <ThemeProvider>
        <Component {...pageProps} />
      </ThemeProvider>
    </AuthProvider>
  );
}