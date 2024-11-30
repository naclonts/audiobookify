// frontend/src/services/api.js

import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const uploadPDF = (formData) => {
  return axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const checkStatus = (taskId) => {
  return axios.get(`${API_BASE_URL}/status/${taskId}`);
};

export const downloadAudio = (taskId) => {
  return axios.get(`${API_BASE_URL}/download/${taskId}`, {
    responseType: 'blob',
  });
};

export const getVoices = () => {
  return axios.get(`${API_BASE_URL}/voices`);
};