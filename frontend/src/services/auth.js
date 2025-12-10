/**
 * Authentication service functions
 */
import api from './api';

export const authService = {
  /**
   * Register a new user
   */
  register: async (email, password, name) => {
    try {
      console.log('Attempting registration with email:', email);
      console.log('API URL:', process.env.REACT_APP_API_URL || 'http://localhost:5000/api');
      
      const response = await api.post('/auth/register', {
        email,
        password,
        name,
      });
      
      console.log('Registration response:', response.data);
      
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      console.error('Full error:', error);
      throw error.response?.data || { error: 'Registration failed' };
    }
  },

  /**
   * Login existing user
   */
  login: async (email, password) => {
    try {
      console.log('Attempting login with email:', email);
      console.log('API URL:', process.env.REACT_APP_API_URL || 'http://localhost:5000/api');
      
      const response = await api.post('/auth/login', {
        email,
        password,
      });
      
      console.log('Login response:', response.data);
      
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      console.error('Full error:', error);
      throw error.response?.data || { error: 'Login failed' };
    }
  },

  /**
   * Logout current user
   */
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },

  /**
   * Get current user from localStorage
   */
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Get current user from API
   */
  getCurrentUserFromAPI: async () => {
    try {
      const response = await api.get('/auth/me');
      return response.data.user;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to get user' };
    }
  },
};

