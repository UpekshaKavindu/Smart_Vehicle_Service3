import { apiClient, aiClient } from './api';

export const customerApi = {
  getAll: () => apiClient.get('/Customer'),
  getById: (id) => apiClient.get(`/Customer/${id}`),
  create: (data) => apiClient.post('/Customer', data),
  update: (id, data) => apiClient.put(`/Customer/${id}`, data),
  delete: (id) => apiClient.delete(`/Customer/${id}`),
  search: (query) => apiClient.get(`/Customer/search?q=${query}`),
};

export const customerAI = {
  setToken: (token) => aiClient.post('/auth/set-token', { token }),
  summary: (customerId, options = {}) => 
    aiClient.post('/customer/summary', {
      customer_id: customerId,
      include_service_history: true,
      include_bookings: true,
      include_maintenance: true,
      specific_question: options.question || null,
    }),
  ask: (customerId, question, maxIterations = 5) =>
    aiClient.post('/customer/ask', {
      customer_id: customerId,
      question,
      max_iterations: maxIterations,
    }),
  graph: (customerId, question, threadId = 'default') =>
    aiClient.post('/customer/graph', {
      customer_id: customerId,
      question,
      thread_id: threadId,
    }),
  resume: (threadId, decision) =>
    aiClient.post('/customer/resume', {
      thread_id: threadId,
      decision,
    }),
  getThread: (threadId) => aiClient.get(`/customer/thread/${threadId}`),
};