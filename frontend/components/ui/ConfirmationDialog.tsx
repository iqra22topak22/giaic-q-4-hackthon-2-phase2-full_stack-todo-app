// frontend/components/ui/ConfirmationDialog.tsx
import React from 'react';
import Modal from './Modal';
import { Button } from './Button';

interface ConfirmationDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title?: string;
  message?: string;
  confirmText?: string;
  cancelText?: string;
  variant?: 'danger' | 'warning' | 'info';
}

const ConfirmationDialog = ({
  isOpen,
  onClose,
  onConfirm,
  title = 'Confirm Action',
  message = 'Are you sure you want to proceed?',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'danger',
}: ConfirmationDialogProps) => {
  const variantColors = {
    danger: {
      button: 'danger',
      icon: 'text-danger-500',
    },
    warning: {
      button: 'warning',
      icon: 'text-warning-500',
    },
    info: {
      button: 'primary',
      icon: 'text-primary-500',
    },
  };

  const currentVariant = variantColors[variant];

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="sm:flex sm:items-start">
        <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-opacity-10 sm:mx-0 sm:h-10 sm:w-10">
          <svg
            className={`h-6 w-6 ${currentVariant.icon}`}
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
          <h3 className="text-lg leading-6 font-medium text-gray-900">{title}</h3>
          <div className="mt-2">
            <p className="text-sm text-gray-500">{message}</p>
          </div>
        </div>
      </div>
      <div className="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
        <Button
          variant={currentVariant.button as any}
          onClick={onConfirm}
          className="ml-3"
        >
          {confirmText}
        </Button>
        <Button
          variant="ghost"
          onClick={onClose}
        >
          {cancelText}
        </Button>
      </div>
    </Modal>
  );
};

export default ConfirmationDialog;