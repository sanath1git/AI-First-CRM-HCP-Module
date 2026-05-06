import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  sendMessage: async (message, currentData = null) => {
    const payload = { message };
    if (currentData) {
      payload.current_data = currentData;
    }
    const response = await api.post('/api/chat', payload);
    return response.data;
  },
};

export const interactionAPI = {
  create: async (data) => {
    const response = await api.post('/api/interactions', data);
    return response.data;
  },

  list: async (params = {}) => {
    const response = await api.get('/api/interactions', { params });
    return response.data;
  },

  get: async (id) => {
    const response = await api.get(`/api/interactions/${id}`);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/api/interactions/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/api/interactions/${id}`);
    return response.data;
  },
};

export default api;

