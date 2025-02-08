import axios from 'axios';
import { toast } from 'react-hot-toast';
import { getToken, removeToken, isTokenValid } from '../utils/auth';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

API.interceptors.request.use(
  async (config) => {
    const token = getToken();
    if (token && isTokenValid()) {
      config.headers.Authorization = `Bearer ${token}`;
    } else if (token) {
      // Token exists but is invalid
      removeToken();
      window.location = '/login';
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      removeToken();
      window.location = '/login';
    }
    
    // Error handling is now done in the specific API calls
    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  login: (credentials) => API.post('/auth/login', credentials),
  register: (userData) => API.post('/auth/register', userData),
  getProfile: () => API.get('/users/me'),
};

export const journalAPI = {
  getEntries: () => API.get('/journal/entries'),
  getEntry: (id) => API.get(`/journal/entries/${id}`),
  createEntry: (entry) => API.post('/journal/entries', entry),
  updateEntry: (id, entry) => API.put(`/journal/entries/${id}`, entry),
  deleteEntry: (id) => API.delete(`/journal/entries/${id}`),
};

export const habitsAPI = {
  getHabits: () => API.get('/habits'),
  createHabit: (habit) => API.post('/habits', habit),
  updateHabit: (id, habit) => API.put(`/habits/${id}`, habit),
  deleteHabit: (id) => API.delete(`/habits/${id}`),
  checkIn: (habitId, data) => API.post(`/habits/${habitId}/checkin`, data),
};

export const analyticsAPI = {
  getJournalStats: () => API.get('/analytics/journal'),
  getHabitStats: () => API.get('/analytics/habits'),
  getMoodTrends: () => API.get('/analytics/mood'),
};

export default API;
