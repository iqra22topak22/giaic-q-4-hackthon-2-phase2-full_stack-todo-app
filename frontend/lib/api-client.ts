import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

// Helper function to safely access localStorage
const getLocalStorage = (): Storage | null => {
  if (typeof window !== 'undefined') {
    return window.localStorage;
  }
  return null;
};

// Create the base API client instance
const createApiClient = (): AxiosInstance => {
  const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://127.0.0.1:8000',
    timeout: 15000, // 15 seconds timeout
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request interceptor to attach JWT token to headers
  apiClient.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      const storage = getLocalStorage();
      if (!storage) {
        return config;
      }

      const token = storage.getItem('jwt_token');
      const userId = storage.getItem('user_id');

      // In development, if using mock-user-id, don't send authorization header
      if (token && !(process.env.NODE_ENV === 'development' && userId && userId === 'mock-user-id')) {
        config.headers = config.headers || {};
        config.headers.Authorization = `Bearer ${token}`;
      }

      // Replace {user_id} placeholder with actual user ID if present in the URL
      if (config.url && userId) {
        config.url = config.url.replace(/{user_id}/g, userId);
      }

      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor to handle errors
  apiClient.interceptors.response.use(
    (response: AxiosResponse) => {
      return response;
    },
    (error) => {
      // Handle different types of errors
      if (error.response) {
        // Server responded with error status
        const { status, data } = error.response;

        // Handle unauthorized access
        if (status === 401) {
          // Clear the token and redirect to login
          const storage = getLocalStorage();
          if (storage) {
            storage.removeItem('jwt_token');
            storage.removeItem('user_id');
          }

          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
          return Promise.reject(error);
        }

        // Handle forbidden access
        if (status === 403) {
          console.error('Forbidden: You do not have permission to access this resource');
        }

        // Handle not found
        if (status === 404) {
          console.error('Not Found: The requested resource was not found');
        }

        // Handle server errors
        if (status >= 500) {
          console.error('Server Error: Something went wrong on our end. Please try again later.');
        }
      } else if (error.request) {
        // Request was made but no response received
        console.error('Network Error: Unable to connect to the server. Please check your connection.');
      } else {
        // Something else happened while setting up the request
        console.error('Error:', error.message);
      }

      return Promise.reject(error);
    }
  );

  return apiClient;
};

const apiClient = typeof window !== 'undefined' ? createApiClient() : axios.create();

export default apiClient;