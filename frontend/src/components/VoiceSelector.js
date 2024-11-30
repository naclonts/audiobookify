// frontend/src/components/VoiceSelector.js

import React, { useEffect, useState } from 'react';
import { getVoices } from '../services/api';

function VoiceSelector({ selectedVoice, setSelectedVoice }) {
  const [voices, setVoices] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchVoices = async () => {
      try {
        const response = await getVoices();
        setVoices(response.data.voices);
      } catch (err) {
        setError('Failed to load available voices.');
        console.error(err);
      }
    };

    fetchVoices();
  }, []);

  const handleChange = (event) => {
    setSelectedVoice(event.target.value);
  };

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (voices.length === 0) {
    return <div>Loading voices...</div>;
  }

  return (
    <div className="voice-selector">
      <h2>Select Voice</h2>
      <select value={selectedVoice} onChange={handleChange}>
        <option value="" disabled>
          -- Choose a voice --
        </option>
        {voices.map((voice) => (
          <option key={voice} value={voice}>
            {voice}
          </option>
        ))}
      </select>
    </div>
  );
}

export default VoiceSelector;
