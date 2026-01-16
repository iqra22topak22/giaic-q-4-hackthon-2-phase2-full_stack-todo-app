// frontend/components/tasks/TaskFetcher.tsx
import React, { useState, useEffect } from 'react';
import { Task } from '../../lib/types';
import apiClient from '../../lib/api-client';
import { getCurrentUserId, setMockUserId } from '../../lib/auth';

interface TaskFetcherProps {
  userId?: string;
}

const TaskFetcher: React.FC<TaskFetcherProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        setError(null);

        // Use the provided userId or get from auth
        let actualUserId = userId || getCurrentUserId();

        // In development, if no user ID is set, use mock-user-id
        if (process.env.NODE_ENV === 'development' && !actualUserId) {
          actualUserId = 'mock-user-id';
          setMockUserId(actualUserId);
        }

        if (!actualUserId) {
          throw new Error('User not authenticated');
        }

        // Make API call to fetch tasks
        // Note: The backend expects the user ID in the URL path as /api/{user_id}/tasks
        const response = await apiClient.get(`/api/${actualUserId}/tasks`);

        console.log('API Response:', response.data);

        // Extract tasks from response based on backend API structure
        // The backend returns data in the format: { tasks: [...], total_count, limit, offset }
        if (response.data && response.data.tasks) {
          // Map backend task structure to frontend Task interface
          const mappedTasks: Task[] = response.data.tasks.map((backendTask: any) => ({
            id: String(backendTask.id),
            title: backendTask.title,
            description: backendTask.description || '',
            status: backendTask.completed ? 'completed' : 'pending',
            createdAt: new Date(backendTask.created_at),
            updatedAt: new Date(backendTask.updated_at),
            userId: backendTask.user_id
          }));

          setTasks(mappedTasks);
        } else {
          setTasks([]);
        }
      } catch (err: any) {
        console.error('Error fetching tasks:', err);
        setError(err.message || 'Failed to fetch tasks');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [userId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-red-700">
              <span className="font-medium">Error:</span> {error}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Fetched Tasks</h2>
      
      {tasks.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500">No tasks found. Create your first task!</p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <div 
              key={task.id} 
              className={`flex items-center justify-between p-4 rounded-lg border ${
                task.status === 'completed'
                  ? 'bg-green-50 border-green-200'
                  : 'bg-white border-gray-200'
              }`}
            >
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={task.status === 'completed'}
                  onChange={() => {}}
                  className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                />
                <span
                  className={`ml-3 text-gray-800 ${
                    task.status === 'completed' ? 'line-through text-gray-500' : ''
                  }`}
                >
                  {task.title}
                </span>
              </div>
              <div className="text-sm text-gray-500">
                {new Date(task.createdAt).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="mt-4 text-sm text-gray-500">
        Total tasks: {tasks.length}
      </div>
    </div>
  );
};

export default TaskFetcher;