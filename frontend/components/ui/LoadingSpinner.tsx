// frontend/components/ui/LoadingSpinner.tsx
import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  color?: 'primary' | 'secondary' | 'gray';
}

const LoadingSpinner = ({ size = 'md', className = '', color = 'primary' }: LoadingSpinnerProps) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  const colorClasses = {
    primary: 'border-primary-500',
    secondary: 'border-secondary-500',
    gray: 'border-gray-400',
  };

  return (
    <div
      className={`inline-block ${sizeClasses[size]} animate-spin rounded-full border-4 border-solid ${colorClasses[color]} border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite] ${className}`}
      role="status"
    >
      <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
        Loading...
      </span>
    </div>
  );
};

export default LoadingSpinner;