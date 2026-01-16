// frontend/components/ui/Modal.tsx
import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
}

const Modal = ({ isOpen, onClose, title, children, size = 'md' }: ModalProps) => {
  const modalRef = useRef<HTMLDivElement>(null);

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
  };

  // Close modal when clicking outside of it
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = 'unset'; // Reset background scrolling
    };
  }, [isOpen, onClose]);

  // Close modal when pressing Escape key
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* Backdrop */}
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" />

        {/* Modal container */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:w-full">
          <div ref={modalRef} className={`${sizeClasses[size]} w-full`}>
            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              {title && (
                <div className="flex items-start justify-between">
                  <h3 className="text-lg font-medium text-gray-900">{title}</h3>
                  <button
                    type="button"
                    className="text-gray-400 hover:text-gray-500 focus:outline-none focus:text-gray-500 transition-colors"
                    onClick={onClose}
                    aria-label="Close"
                  >
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              )}
              <div className="mt-2">
                {children}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>,
    document.body
  );
};

export default Modal;