// frontend/hooks/useTasks.ts
import { useState, useEffect } from 'react';
import apiClient from '../lib/api-client';
import { Task } from '../lib/types';
import { useToast } from '../contexts/ToastContext';

export const useTasks = () => {
  const { showToast } = useToast();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch all tasks
  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null); // Reset error state
      const response = await apiClient.get<{ success: boolean; data?: Task[]; message?: string }>('/tasks');

      if (response.data.success && response.data.data) {
        setTasks(response.data.data);
      } else {
        const errorMsg = response.data.message || 'Failed to fetch tasks';
        setError(errorMsg);
        showToast(errorMsg, 'error');
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'An error occurred while fetching tasks';
      setError(errorMsg);
      showToast(errorMsg, 'error');
      console.error('Fetch tasks error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Create a new task
  const createTask = async (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'userId'>) => {
    try {
      setLoading(true);
      const response = await apiClient.post<{ success: boolean; data?: Task; message?: string }>('/tasks', taskData);

      if (response.data.success && response.data.data) {
        setTasks([...tasks, response.data.data]);
        showToast('Task created successfully', 'success');
        return response.data.data;
      } else {
        const errorMsg = response.data.message || 'Failed to create task';
        setError(errorMsg);
        showToast(errorMsg, 'error');
        return null;
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'An error occurred while creating the task';
      setError(errorMsg);
      showToast(errorMsg, 'error');
      console.error('Create task error:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Update an existing task
  const updateTask = async (id: string, taskData: Partial<Task>) => {
    try {
      setLoading(true);
      const response = await apiClient.put<{ success: boolean; data?: Task; message?: string }>(`/tasks/${id}`, taskData);

      if (response.data.success && response.data.data) {
        setTasks(tasks.map(task => task.id === id ? response.data.data! : task));
        showToast('Task updated successfully', 'success');
        return response.data.data;
      } else {
        const errorMsg = response.data.message || 'Failed to update task';
        setError(errorMsg);
        showToast(errorMsg, 'error');
        return null;
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'An error occurred while updating the task';
      setError(errorMsg);
      showToast(errorMsg, 'error');
      console.error('Update task error:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Delete a task
  const deleteTask = async (id: string) => {
    try {
      setLoading(true);
      const response = await apiClient.delete<{ success: boolean; message?: string }>(`/tasks/${id}`);

      if (response.data.success) {
        setTasks(tasks.filter(task => task.id !== id));
        showToast('Task deleted successfully', 'success');
        return true;
      } else {
        const errorMsg = response.data.message || 'Failed to delete task';
        setError(errorMsg);
        showToast(errorMsg, 'error');
        return false;
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || 'An error occurred while deleting the task';
      setError(errorMsg);
      showToast(errorMsg, 'error');
      console.error('Delete task error:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Filter tasks by status
  const filterTasks = (status: 'pending' | 'completed' | 'all') => {
    if (status === 'all') {
      return tasks;
    }
    return tasks.filter(task => task.status === status);
  };

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    filterTasks,
  };
};