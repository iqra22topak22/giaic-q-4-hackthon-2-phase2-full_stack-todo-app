import React, { useState, useEffect } from 'react';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskSummaryData {
  totalTasks: number;
  completedTasks: number;
  pendingTasks: number;
  completionPercentage: number;
}

const TaskSummary: React.FC = () => {
  const [summary, setSummary] = useState<TaskSummaryData>({
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0,
    completionPercentage: 0,
  });

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);

        // Get the user ID from localStorage
        const userId = localStorage.getItem('user_id');
        if (!userId) {
          throw new Error('User not authenticated');
        }

        // Construct the API URL using the environment variable
        const apiUrl = `${process.env.NEXT_PUBLIC_BACKEND_API_URL}/api/${userId}/tasks`;

        const response = await fetch(apiUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // Include authorization header if needed
            'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
          }
        });

        if (!response.ok) {
          throw new Error(`API request failed with status ${response.status}`);
        }

        const data = await response.json();

        if (data && data.tasks) {
          const tasks: Task[] = data.tasks;

          const totalTasks = tasks.length;
          const completedTasks = tasks.filter(task => task.completed).length;
          const pendingTasks = tasks.filter(task => !task.completed).length;

          const completionPercentage = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

          setSummary({
            totalTasks,
            completedTasks,
            pendingTasks,
            completionPercentage,
          });
        }

        setError(null);
      } catch (err) {
        console.error('Error fetching tasks:', err);
        setError('Failed to load task statistics. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-6">Statistics</h2>
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-6">Statistics</h2>
        <div className="text-red-500 text-center py-10">{error}</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6">Statistics</h2>
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-blue-700">{summary.totalTasks}</p>
          <p className="text-gray-600">Total Tasks</p>
        </div>
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-green-700">{summary.completedTasks}</p>
          <p className="text-gray-600">Completed</p>
        </div>
        <div className="bg-yellow-50 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-yellow-700">{summary.pendingTasks}</p>
          <p className="text-gray-600">Pending</p>
        </div>
      </div>

      <div>
        <div className="flex justify-between mb-2">
          <span className="text-gray-600">Completion Rate</span>
          <span className="font-bold text-gray-800">{summary.completionPercentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-green-600 h-2.5 rounded-full"
            style={{ width: `${summary.completionPercentage}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default TaskSummary;