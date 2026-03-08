import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

export const getSummary = () => api.get('/api/summary');
export const getAllocation = () => api.get('/api/charts/allocation');
export const getCountryCharts = () => api.get('/api/charts/country');
export const getTrends = () => api.get('/api/charts/trends');
export const getCategories = () => api.get('/api/charts/categories');
export const getTransactions = () => api.get('/api/transactions');

export default api;
