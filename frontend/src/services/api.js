import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '/api';

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