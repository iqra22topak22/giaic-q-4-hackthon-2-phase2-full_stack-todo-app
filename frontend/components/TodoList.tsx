import { useState, useEffect } from 'react';
import apiClient from '../lib/api-client'; // Import the axios client

interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TodoListProps {
  userId: string;
  onTaskChange?: () => void;
}

export default function TodoList({ userId, onTaskChange }: TodoListProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(true);

  // Fetch tasks from backend via direct API call
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        // Using the axios client to call FastAPI backend directly
        const response = await apiClient.get(`/api/${userId}/tasks`);
        if (response.status === 200) {
          setTodos(response.data.tasks || []);
        } else {
          console.error('Failed to fetch tasks:', response.status);
        }
      } catch (error) {
        console.error('Error fetching tasks:', error);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchTodos();
    }
  }, [userId]);

  const addTodo = async () => {
    if (inputValue.trim() !== '') {
      try {
        const response = await apiClient.post(`/api/${userId}/tasks`, {
          title: inputValue,
          description: '',
          completed: false,
        });

        if (response.status === 201) {
          setTodos([...todos, response.data.data]);
          setInputValue('');
          if (onTaskChange) onTaskChange(); // Trigger parent to refresh stats
        } else {
          console.error('Failed to add task:', response.status);
        }
      } catch (error) {
        console.error('Error adding task:', error);
      }
    }
  };

  const toggleTodo = async (id: number) => {
    try {
      const response = await apiClient.put(`/api/${userId}/tasks/${id}`, {
        completed: !todos.find(todo => todo.id === id)?.completed,
      });

      if (response.status === 200) {
        setTodos(
          todos.map(todo =>
            todo.id === id ? response.data.data : todo
          )
        );
        if (onTaskChange) onTaskChange(); // Trigger parent to refresh stats
      } else {
        console.error('Failed to update task:', response.status);
      }
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const deleteTodo = async (id: number) => {
    try {
      const response = await apiClient.delete(`/api/${userId}/tasks/${id}`);

      if (response.status === 200) {
        setTodos(todos.filter(todo => todo.id !== id));
        if (onTaskChange) onTaskChange(); // Trigger parent to refresh stats
      } else {
        console.error('Failed to delete task:', response.status);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-gray-500 mt-4">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex gap-2 mb-6">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && addTodo()}
          placeholder="Add a new task..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          onClick={addTodo}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition duration-200"
        >
          Add
        </button>
      </div>

      <div className="space-y-3">
        {todos.map((todo) => (
          <div
            key={todo.id}
            className={`flex items-center justify-between p-4 rounded-lg border ${
              todo.completed
                ? 'bg-green-50 border-green-200'
                : 'bg-white border-gray-200'
            }`}
          >
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleTodo(todo.id)}
                className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
              />
              <span
                className={`ml-3 text-gray-800 ${
                  todo.completed ? 'line-through text-gray-500' : ''
                }`}
              >
                {todo.title}
              </span>
            </div>
            <button
              onClick={() => deleteTodo(todo.id)}
              className="text-red-500 hover:text-red-700"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        ))}
      </div>

      {todos.length === 0 && (
        <div className="text-center py-8">
          <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <p className="text-gray-500 text-lg">No tasks yet. Add your first task!</p>
        </div>
      )}
    </div>
  );
}