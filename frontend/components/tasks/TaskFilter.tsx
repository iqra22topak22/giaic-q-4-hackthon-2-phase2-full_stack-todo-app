// frontend/components/tasks/TaskFilter.tsx
import React from 'react';
import { Button } from '../ui/Button';

interface TaskFilterProps {
  currentFilter: 'all' | 'pending' | 'completed';
  onFilterChange: (filter: 'all' | 'pending' | 'completed') => void;
  onSortChange?: (sortOption: string) => void;
}

const TaskFilter = ({ currentFilter, onFilterChange, onSortChange }: TaskFilterProps) => {
  const filterOptions = [
    { id: 'all', label: 'All Tasks' },
    { id: 'pending', label: 'Pending' },
    { id: 'completed', label: 'Completed' },
  ];

  const sortOptions = [
    { id: 'title-asc', label: 'Title A-Z' },
    { id: 'title-desc', label: 'Title Z-A' },
    { id: 'date-newest', label: 'Newest First' },
    { id: 'date-oldest', label: 'Oldest First' },
  ];

  return (
    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <div className="flex space-x-2">
        {filterOptions.map((option) => (
          <Button
            key={option.id}
            variant={currentFilter === option.id ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => onFilterChange(option.id as 'all' | 'pending' | 'completed')}
          >
            {option.label}
          </Button>
        ))}
      </div>

      {onSortChange && (
        <div className="flex items-center">
          <label htmlFor="sort-select" className="mr-2 text-sm text-gray-600">
            Sort by:
          </label>
          <select
            id="sort-select"
            className="border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            onChange={(e) => onSortChange(e.target.value)}
          >
            {sortOptions.map((option) => (
              <option key={option.id} value={option.id}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
};

export default TaskFilter;