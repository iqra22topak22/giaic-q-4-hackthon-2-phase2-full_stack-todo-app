import Head from 'next/head';
import Link from 'next/link';

export default function Custom404() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Head>
        <title>Page Not Found | Todo App</title>
        <meta name="description" content="Page not found" />
      </Head>

      <main className="flex-grow flex items-center justify-center p-4">
        <div className="text-center max-w-md">
          <div className="text-6xl font-bold text-gray-300 mb-4">404</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-4">Page Not Found</h1>
          <p className="text-gray-600 mb-8">
            Sorry, we couldn't find the page you're looking for.
          </p>
          <Link href="/">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-200">
              Go Back Home
            </button>
          </Link>
        </div>
      </main>
    </div>
  );
}