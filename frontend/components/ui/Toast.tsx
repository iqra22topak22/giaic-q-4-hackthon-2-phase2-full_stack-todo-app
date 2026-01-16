// frontend/components/ui/Toast.tsx
'use client';

import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';

interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onClose?: () => void;
}

const Toast = ({ message, type = 'info', duration = 3000, onClose }: ToastProps) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
      if (onClose) {
        onClose();
      }
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const typeClasses = {
    success: 'bg-success-500 text-white',
    error: 'bg-danger-500 text-white',
    warning: 'bg-warning-500 text-gray-900',
    info: 'bg-primary-500 text-white',
  };

  if (!visible) return null;

  return createPortal(
    <div className={`fixed bottom-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg transform transition-transform duration-300 ease-in-out ${typeClasses[type]} ${visible ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'}`}>
      <div className="flex items-center">
        <span className="mr-2">{message}</span>
        <button
          onClick={() => {
            setVisible(false);
            if (onClose) onClose();
          }}
          className="ml-4 text-current hover:opacity-75 focus:outline-none"
          aria-label="Close toast"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>,
    document.body
  );
};

export default Toast;