import { useState, useEffect } from 'react';
import { Task } from '../lib/types';
import { isAuthenticated } from '../lib/auth';
import { useRouter } from 'next/router';
import apiClient from '../lib/api-client';
import Header from '../components/Header';
import TaskList from '../components/tasks/TaskList';
import TaskForm from '../components/tasks/TaskForm';
import BulkTaskForm from '../components/tasks/BulkTaskForm';
import { Button } from '../components/ui/Button';
import { Plus, Upload } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Dashboard() {
  const router = useRouter();
  const { userSession } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showBulkForm, setShowBulkForm] = useState(false);

  const pendingTasks = tasks.filter(task => task.status === 'pending');

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
      setError(null);

      const userId = userSession?.userId;
      if (!userId) {
        throw new Error('User ID not found');
      }

      const response = await apiClient.get(`/api/${userId}/tasks`);

      if (response.data && response.data.tasks) {
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

  const handleAddTask = async (taskData: Partial<Task>) => {
    try {
      setError(null);

      const userId = userSession?.userId;
      if (!userId) {
        throw new Error('User ID not found');
      }

      const response = await apiClient.post(`/api/${userId}/tasks`, {
        title: taskData.title,
        description: taskData.description,
        completed: taskData.status === 'completed'
      });

      const newTask: Task = {
        id: String(response.data.data.id),
        title: response.data.data.title,
        description: response.data.data.description,
        status: response.data.data.completed ? 'completed' : 'pending',
        createdAt: new Date(response.data.data.created_at),
        updatedAt: new Date(response.data.data.updated_at),
        userId: response.data.data.user_id
      };

      setTasks([newTask, ...tasks]);
      setShowAddForm(false);
    } catch (err: any) {
      console.error('Error adding task:', err);
      setError(err.message || 'Failed to add task');
    }
  };

  const handleBulkAddTasks = async (tasksData: Partial<Task>[]) => {
    try {
      setError(null);

      const userId = userSession?.userId;
      if (!userId) {
        throw new Error('User ID not found');
      }

      // Prepare the bulk request payload
      const bulkPayload = {
        tasks: tasksData.map(task => ({
          title: task.title || '',
          description: task.description || '',
          completed: task.status === 'completed'
        }))
      };

      const response = await apiClient.post(`/api/${userId}/tasks/bulk`, bulkPayload);

      // Convert response to Task objects
      const newTasks: Task[] = response.data.data.map((backendTask: any) => ({
        id: String(backendTask.id),
        title: backendTask.title,
        description: backendTask.description || '',
        status: backendTask.completed ? 'completed' : 'pending',
        createdAt: new Date(backendTask.created_at),
        updatedAt: new Date(backendTask.updated_at),
        userId: backendTask.user_id
      }));

      // Add new tasks to the beginning of the list
      setTasks([...newTasks, ...tasks]);
      setShowBulkForm(false);
    } catch (err: any) {
      console.error('Error adding multiple tasks:', err);
      setError(err.message || 'Failed to add multiple tasks');
    }
  };

  const handleToggleTask = async (taskId: string) => {
    try {
      setError(null);

      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      const userId = userSession?.userId;
      if (!userId) {
        throw new Error('User ID not found');
      }

      const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`, {
        completed: task.status !== 'completed'
      });

      setTasks(tasks.map(t =>
        t.id === taskId
          ? { ...t, status: t.status === 'completed' ? 'pending' : 'completed' }
          : t
      ));
    } catch (err: any) {
      console.error('Error toggling task:', err);
      setError(err.message || 'Failed to update task');
    }
  };

  const handleUpdateTask = async (taskId: string, updatedTask: Partial<Task>) => {
    try {
      setError(null);

      const userId = userSession?.userId;
      if (!userId) {
        throw new Error('User ID not found');
      }

      const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, {
        title: updatedTask.title,
        description: updatedTask.description,
        completed: updatedTask.status === 'completed'
      });

      setTasks(tasks.map(t =>
        t.id === taskId
          ? {
              ...t,
              title: updatedTask.title || t.title,
              description: updatedTask.description || t.description,
              status: updatedTask.status || t.status,
              updatedAt: new Date(response.data.data.updated_at)
            }
          : t
      ));
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      setError(null);

      const userId = userSession?.userId;
      if (!userId) {
        throw new Error('User ID not found');
      }

      await apiClient.delete(`/api/${userId}/tasks/${taskId}`);

      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (err: any) {
      console.error('Error deleting task:', err);
      setError(err.message || 'Failed to delete task');
    }
  };

  if (!isAuthenticated()) {
    return null; // Redirect will happen in useEffect
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <Header />

      <main className="container py-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 dark:text-white">My Tasks</h1>
              <p className="text-gray-600 dark:text-gray-300 mt-1">
                {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} • {pendingTasks.length} pending
              </p>
            </div>
            <div className="flex gap-2">
              <Button
                onClick={() => setShowBulkForm(true)}
                className="bg-green-600 hover:bg-green-700 text-white flex items-center gap-2 px-4 py-2 rounded-lg transition-all transform hover:scale-105"
              >
                <Upload className="h-4 w-4" />
                <span>Bulk Add</span>
              </Button>
              <Button
                onClick={() => setShowAddForm(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-2 px-4 py-2 rounded-lg transition-all transform hover:scale-105"
              >
                <Plus className="h-4 w-4" />
                <span>Add Task</span>
              </Button>
            </div>
          </div>

          {showAddForm && (
            <div className="mb-6 animate-fade-in">
              <TaskForm
                onSave={(taskData) => {
                  handleAddTask(taskData);
                  setShowAddForm(false);
                }}
                onCancel={() => setShowAddForm(false)}
              />
            </div>
          )}

          {showBulkForm && (
            <div className="mb-6 animate-fade-in">
              <BulkTaskForm
                isOpen={showBulkForm}
                onClose={() => setShowBulkForm(false)}
                onBulkSave={(tasksData) => {
                  handleBulkAddTasks(tasksData);
                }}
              />
            </div>
          )}

          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-all duration-300 hover:shadow-xl">
            <TaskList
              tasks={tasks}
              loading={loading}
              error={error}
              onToggle={handleToggleTask}
              onDelete={handleDeleteTask}
              onUpdate={handleUpdateTask}
            />
          </div>
        </div>
      </main>
    </div>
  );
}