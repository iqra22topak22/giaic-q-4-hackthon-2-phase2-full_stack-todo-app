// frontend/components/layout/Header.tsx
'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/Button';

const Header = () => {
  const { userSession, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-primary-600">Todo App</Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-4">
            {userSession?.isAuthenticated ? (
              <>
                <Link href="/dashboard" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                  Dashboard
                </Link>
                <Button variant="ghost" onClick={logout}>
                  Sign Out
                </Button>
              </>
            ) : (
              <>
                <Link href="/signin">
                  <Button variant="ghost">Sign In</Button>
                </Link>
                <Link href="/signup">
                  <Button variant="primary">Sign Up</Button>
                </Link>
              </>
            )}
          </nav>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-primary-600 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
              aria-controls="mobile-menu"
              aria-expanded={mobileMenuOpen}
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <span className="sr-only">Open main menu</span>
              {!mobileMenuOpen ? (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              ) : (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden" id="mobile-menu">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {userSession?.isAuthenticated ? (
              <>
                <Link href="/dashboard" className="text-gray-700 hover:text-primary-600 block px-3 py-2 rounded-md text-base font-medium">
                  Dashboard
                </Link>
                <button
                  onClick={logout}
                  className="w-full text-left text-gray-700 hover:text-primary-600 block px-3 py-2 rounded-md text-base font-medium"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <Link href="/signin" className="text-gray-700 hover:text-primary-600 block px-3 py-2 rounded-md text-base font-medium">
                  Sign In
                </Link>
                <Link href="/signup" className="text-gray-700 hover:text-primary-600 block px-3 py-2 rounded-md text-base font-medium">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;