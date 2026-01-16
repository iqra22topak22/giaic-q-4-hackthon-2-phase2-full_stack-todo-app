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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <Head>
        <title>Welcome - Todo App</title>
        <meta name="description" content="Welcome to the Todo App" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="w-full max-w-md text-center">
        <div className="mb-10">
          <div className="mx-auto bg-blue-600 w-16 h-16 rounded-xl flex items-center justify-center mb-4">
            <h1 className="text-2xl font-bold text-white">Todo</h1>
          </div>
          <h1 className="text-3xl font-bold text-gray-800">Welcome to Todo App</h1>
          <p className="text-gray-600 mt-2">Organize your tasks efficiently</p>
        </div>

        <div className="space-y-4">
          <Link href="/login">
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium transition duration-200 transform hover:scale-[1.02]">
              Sign In
            </button>
          </Link>

          <Link href="/signup">
            <button className="w-full bg-white hover:bg-gray-100 text-gray-800 border border-gray-300 py-3 px-4 rounded-lg font-medium transition duration-200 transform hover:scale-[1.02]">
              Sign Up
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}