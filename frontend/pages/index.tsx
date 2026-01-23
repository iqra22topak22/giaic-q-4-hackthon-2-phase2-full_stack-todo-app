import Head from 'next/head';
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { isAuthenticated } from '../lib/auth';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    if (isAuthenticated()) {
      // If authenticated, redirect to dashboard
      router.push('/dashboard');
    }
    // Note: We don't redirect to login immediately anymore
    // Instead, we show the welcome page with login/signup options
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <Head>
        <title>Welcome - Todo App</title>
        <meta name="description" content="Welcome to the Todo App" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="w-full max-w-md text-center">
        <div className="mb-10">
          <div className="mx-auto bg-gradient-to-r from-blue-500 to-indigo-600 w-20 h-20 rounded-2xl flex items-center justify-center mb-6 shadow-lg">
            <h1 className="text-3xl font-bold text-white">Todo</h1>
          </div>
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-3">Welcome to Todo App</h1>
          <p className="text-gray-600 dark:text-gray-300 text-lg">Organize your tasks efficiently</p>
        </div>

        <div className="space-y-4">
          <Link href="/login">
            <button className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white py-4 px-6 rounded-xl font-semibold text-base transition-all duration-300 transform hover:scale-[1.02] shadow-lg">
              Sign In
            </button>
          </Link>

          <Link href="/signup">
            <button className="w-full bg-gradient-to-r from-white to-gray-100 dark:from-gray-800 dark:to-gray-700 hover:from-gray-100 hover:to-gray-200 dark:hover:from-gray-700 dark:hover:to-gray-600 text-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 py-4 px-6 rounded-xl font-semibold text-base transition-all duration-300 transform hover:scale-[1.02] shadow-lg">
              Sign Up
            </button>
          </Link>
        </div>

        <div className="mt-8 text-center">
          <p className="text-gray-500 dark:text-gray-400 text-sm">
            By signing up, you agree to our Terms and Privacy Policy.
          </p>
        </div>
      </div>
    </div>
  );
}