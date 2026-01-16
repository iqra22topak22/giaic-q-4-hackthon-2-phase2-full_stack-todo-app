import Head from 'next/head';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { isAuthenticated, signOut, getCurrentUserId } from '../lib/auth';
import AuthGuard from '../components/AuthGuard';
import apiClient from '../lib/api-client';
import { Task } from '../lib/types';
import Header from '../components/Header';

export default function Tasks() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Check authentication on mount
  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
    } else {
      fetchTasks();
    }
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Get user ID from localStorage
      const userId = getCurrentUserId();
      if (!userId) {
        throw new Error('User ID not found');
      }

      const response = await apiClient.get(`/api/${userId}/tasks`);
      
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

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      setError('Task title is required');
      return;
    }

    try {
      setError('');

      // Get user ID from localStorage
      const userId = getCurrentUserId();
      if (!userId) {
        throw new Error('User ID not found');
      }

      const response = await apiClient.post(`/api/${userId}/tasks`, {
        title: newTaskTitle,
        description: newTaskDescription,
        completed: false
      });

      // Add the new task to the list
      const newTask: Task = {
        id: String(response.data.data.id),
        title: response.data.data.title,
        description: response.data.data.description || '',
        status: response.data.data.completed ? 'completed' : 'pending',
        createdAt: new Date(response.data.data.created_at),
        updatedAt: new Date(response.data.data.updated_at),
        userId: response.data.data.user_id
      };

      setTasks([...tasks, newTask]);
      setNewTaskTitle('');
      setNewTaskDescription('');
    } catch (err: any) {
      console.error('Error adding task:', err);
      if (err.response) {
        setError(`Failed to add task: ${err.response.data.detail || err.response.statusText}`);
      } else if (err.request) {
        setError('Network error: Unable to connect to the server. Please check your connection.');
      } else {
        setError(err.message || 'Failed to add task');
      }
    }
  };

  const handleToggleTask = async (taskId: string) => {
    try {
      setError('');
      
      // Find the task in the list
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      // Get user ID from localStorage
      const userId = getCurrentUserId();
      if (!userId) {
        throw new Error('User ID not found');
      }

      const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`, {
        completed: !task.status.includes('completed')
      });
      
      // Update the task in the list
      setTasks(tasks.map(t => 
        t.id === taskId 
          ? { ...t, status: t.status.includes('completed') ? 'pending' : 'completed' } 
          : t
      ));
    } catch (err: any) {
      console.error('Error toggling task:', err);
      setError(err.message || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      setError('');
      
      // Get user ID from localStorage
      const userId = getCurrentUserId();
      if (!userId) {
        throw new Error('User ID not found');
      }

      await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
      
      // Remove the task from the list
      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (err: any) {
      console.error('Error deleting task:', err);
      setError(err.message || 'Failed to delete task');
    }
  };


  if (!isAuthenticated()) {
    return null; // AuthGuard will handle redirect
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <Head>
          <title>Tasks - Todo App</title>
          <meta name="description" content="Manage your tasks" />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <Header />

        <main className="container mx-auto px-4 py-8 max-w-4xl">
          <div className="mb-10 text-center">
            <h1 className="text-3xl font-bold text-gray-800">My Tasks</h1>
            <p className="text-gray-600 mt-2">Manage your tasks and track your progress</p>
          </div>

          {/* Add Task Form */}
          <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Add New Task</h2>
            <form onSubmit={handleAddTask} className="space-y-4">
              <div>
                <label htmlFor="taskTitle" className="block text-sm font-medium text-gray-700 mb-1">
                  Task Title *
                </label>
                <input
                  id="taskTitle"
                  type="text"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="What needs to be done?"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="taskDescription" className="block text-sm font-medium text-gray-700 mb-1">
                  Description (Optional)
                </label>
                <textarea
                  id="taskDescription"
                  value={newTaskDescription}
                  onChange={(e) => setNewTaskDescription(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Add details..."
                  rows={3}
                />
              </div>
              
              <button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium transition duration-200"
              >
                Add Task
              </button>
            </form>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Tasks List */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-gray-800">My Tasks</h2>
              <span className="text-gray-600">{tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}</span>
            </div>

            {loading ? (
              <div className="flex justify-center items-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
              </div>
            ) : tasks.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">No tasks yet. Add your first task!</p>
              </div>
            ) : (
              <div className="space-y-4">
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
                        onChange={() => handleToggleTask(task.id)}
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
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        Delete
                      </button>
                      <span className="text-sm text-gray-500">
                        {new Date(task.createdAt).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </main>
      </div>
    </AuthGuard>
  );
}