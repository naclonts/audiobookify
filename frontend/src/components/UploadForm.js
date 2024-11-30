// frontend/src/components/UploadForm.js

import React, { useState } from 'react';
import { uploadPDF, checkStatus } from '../services/api';
import VoiceSelector from './VoiceSelector';
import AudioPlayer from './AudioPlayer';

function UploadForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedVoice, setSelectedVoice] = useState('');
  const [taskId, setTaskId] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setError('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setError('Please select a PDF file to upload.');
      return;
    }

    if (!selectedVoice) {
      setError('Please select a voice.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('voice', selectedVoice); // Ensure backend accepts 'voice'

    try {
      const response = await uploadPDF(formData);
      setTaskId(response.data.task_id);
      setStatus(response.data.status);
      pollStatus(response.data.task_id);
    } catch (err) {
      setError('Failed to upload the PDF. Please try again.');
      console.error(err);
    }
  };

  const pollStatus = async (taskId) => {
    const interval = setInterval(async () => {
      try {
        const response = await checkStatus(taskId);
        setStatus(response.data.status);

        if (response.data.status === 'completed') {
          clearInterval(interval);
        } else if (response.data.status === 'failed') {
          clearInterval(interval);
          setError('The conversion task failed. Please try again.');
        }
      } catch (err) {
        clearInterval(interval);
        setError('Failed to retrieve task status.');
        console.error(err);
      }
    }, 3000); // Poll every 3 seconds
  };

  return (
    <div className="upload-form">
      <h2>Upload PDF</h2>
      <form onSubmit={handleSubmit}>
        <VoiceSelector selectedVoice={selectedVoice} setSelectedVoice={setSelectedVoice} />
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button type="submit">Convert to Speech</button>
      </form>
      {status && (
        <div className="status">
          <p>Task ID: {taskId}</p>
          <p>Status: {status}</p>
        </div>
      )}
      {error && <div className="error">{error}</div>}
      {status === 'completed' && <AudioPlayer taskId={taskId} />}
    </div>
  );
}

export default UploadForm;
