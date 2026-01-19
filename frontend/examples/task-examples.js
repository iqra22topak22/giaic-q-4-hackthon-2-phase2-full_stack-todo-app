// Example frontend fetch code for interacting with the task API
// These examples show how to make requests to the backend directly
// Uses environment variable for the backend URL to work in both dev and prod

// Helper function to get the backend API URL
function getBackendApiUrl() {
  return process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://127.0.0.1:8000';
}

// GET all tasks for a user
export async function getTasks(userId) {
  try {
    const response = await fetch(`${getBackendApiUrl()}/api/${userId}/tasks`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Retrieved tasks:', data);
    return data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
}

// POST a new task for a user
export async function createTask(userId, taskData) {
  try {
    const response = await fetch(`${getBackendApiUrl()}/api/${userId}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Created task:', data);
    return data;
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
}

// GET a specific task for a user
export async function getTask(userId, taskId) {
  try {
    const response = await fetch(`${getBackendApiUrl()}/api/${userId}/tasks/${taskId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Retrieved task:', data);
    return data;
  } catch (error) {
    console.error('Error fetching task:', error);
    throw error;
  }
}

// PUT (update) a specific task for a user
export async function updateTask(userId, taskId, taskData) {
  try {
    const response = await fetch(`${getBackendApiUrl()}/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Updated task:', data);
    return data;
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
}

// DELETE a specific task for a user
export async function deleteTask(userId, taskId) {
  try {
    const response = await fetch(`${getBackendApiUrl()}/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Deleted task:', data);
    return data;
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
}

// PATCH (toggle completion) for a specific task
export async function toggleTaskCompletion(userId, taskId, completed) {
  try {
    const response = await fetch(`${getBackendApiUrl()}/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ completed }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Toggled task completion:', data);
    return data;
  } catch (error) {
    console.error('Error toggling task completion:', error);
    throw error;
  }
}