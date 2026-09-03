import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';
const AI_BASE = import.meta.env.VITE_AI_BASE_URL || '/ai';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

export const aiClient = axios.create({
  baseURL: AI_BASE,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);