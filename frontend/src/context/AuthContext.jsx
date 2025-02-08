import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api/client';
import { setToken, removeToken, isTokenValid, getToken } from '../utils/auth';
import { toast } from 'react-hot-toast';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [initialized, setInitialized] = useState(false);

  const fetchUserProfile = async () => {
    try {
      const { data } = await authAPI.getProfile();
      setUser(data);
    } catch (error) {
      removeToken();
      setUser(null);
    }
  };

  useEffect(() => {
    const initializeAuth = async () => {
      const token = getToken();
      if (token && isTokenValid()) {
        await fetchUserProfile();
      } else if (token) {
        removeToken();
      }
      setLoading(false);
      setInitialized(true);
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const { data } = await authAPI.login({ email, password });
      setToken(data.access_token);
      await fetchUserProfile();
      toast.success('Welcome back!');
      return data;
    } catch (error) {
      const detail = error.response?.data?.detail;
      const message = typeof detail === 'object' ? JSON.stringify(detail) : detail || 'Login failed';
      toast.error(message);
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const { data } = await authAPI.register(userData);
      setToken(data.access_token);
      await fetchUserProfile();
      toast.success('Registration successful!');
      return data;
    } catch (error) {
      const detail = error.response?.data?.detail;
      const message = typeof detail === 'object' ? JSON.stringify(detail) : detail || 'Registration failed';
      toast.error(message);
      throw error;
    }
  };

  const logout = () => {
    removeToken();
    setUser(null);
    toast.success('Logged out successfully');
  };

  if (!initialized || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-mind-blue" />
      </div>
    );
  }

  const value = {
    user,
    login,
    logout,
    register,
    isAuthenticated: !!user,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
