// frontend/src/components/AudioPlayer.js

import React, { useEffect, useState } from 'react';
import { downloadAudio } from '../services/api';

function AudioPlayer({ taskId }) {
  const [audioUrl, setAudioUrl] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAudio = async () => {
      try {
        const response = await downloadAudio(taskId);
        const blob = new Blob([response.data], { type: 'audio/wav' });
        const url = window.URL.createObjectURL(blob);
        setAudioUrl(url);
      } catch (err) {
        setError('Failed to load audio. Please try again.');
        console.error(err);
      }
    };

    if (taskId) {
      fetchAudio();
    }

    // Cleanup the object URL when the component unmounts
    return () => {
      if (audioUrl) {
        window.URL.revokeObjectURL(audioUrl);
      }
    };
  }, [taskId, audioUrl]);

  const handleDownload = () => {
    if (!audioUrl) return;
    const link = document.createElement('a');
    link.href = audioUrl;
    link.setAttribute('download', `audio_${taskId}.wav`);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  };

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!audioUrl) {
    return <div>Loading audio...</div>;
  }

  return (
    <div className="audio-player">
      <h3>Generated Audio</h3>
      <audio controls>
        <source src={audioUrl} type="audio/wav" />
        Your browser does not support the audio element.
      </audio>
      <br />
      <button onClick={handleDownload}>Download Audio</button>
    </div>
  );
}

export default AudioPlayer;
