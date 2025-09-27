import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const chatAPI = {
  sendMessage: async (message, conversationId = null, temperature = 0.7, maxTokens = 1024) => {
    try {
      const response = await api.post('/chat', {
        message,
        conversation_id: conversationId,
        temperature,
        max_tokens: maxTokens
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to send message');
    }
  },

  getModelStatus: async () => {
    try {
      const response = await api.get('/status');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get model status');
    }
  },

  reloadModel: async () => {
    try {
      const response = await api.post('/reload');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to reload model');
    }
  }
};

export default api;
