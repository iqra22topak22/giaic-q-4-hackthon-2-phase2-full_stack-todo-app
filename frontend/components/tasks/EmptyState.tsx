// frontend/components/tasks/EmptyState.tsx
import React from 'react';
import { Card } from '../ui/Card';
import Link from 'next/link';
import { Button } from '../ui/Button';

interface EmptyStateProps {
  title?: string;
  message?: string;
  actionText?: string;
  actionLink?: string;
  onActionClick?: () => void;
}

const EmptyState = ({
  title = 'No tasks yet',
  message = 'Get started by creating your first task',
  actionText = 'Create Task',
  actionLink = '/tasks/new',
  onActionClick
}: EmptyStateProps) => {
  return (
    <Card className="text-center py-12" variant="elevated">
      <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-primary-100">
        <svg
          className="h-8 w-8 text-primary-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
      </div>
      <h3 className="mt-4 text-xl font-medium text-gray-900">{title}</h3>
      <p className="mt-2 text-gray-500 max-w-md mx-auto">{message}</p>
      <div className="mt-6">
        {onActionClick ? (
          <Button variant="primary" onClick={onActionClick}>
            {actionText}
          </Button>
        ) : (
          <Link href={actionLink}>
            <Button variant="primary">
              {actionText}
            </Button>
          </Link>
        )}
      </div>
    </Card>
  );
};

export default EmptyState;