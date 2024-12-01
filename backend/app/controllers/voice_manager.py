# backend/app/controllers/voice_manager.py

import torch
from datasets import load_dataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class VoiceManager:
    """
    Manages available TTS voices and their corresponding embeddings.
    """

    def __init__(self):
        # Load speaker embeddings
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        # Create a mapping of voice names to embedding indices
        self.voices = self.load_available_voices()

    def load_available_voices(self):
        """
        Loads available voices and creates a mapping.
        """
        # Map voice names to indices in the embeddings_dataset
        voices = {
            'cmu_us_bdl_arctic': 7306,
            'cmu_us_clb_arctic': 7307,
            'cmu_us_jmk_arctic': 7308,
            'cmu_us_slt_arctic': 7309,
            # Add more mappings as needed
        }
        return voices

    def get_available_voices(self):
        """
        Returns a list of available voice names.
        """
        return list(self.voices.keys())

    def get_voice_embedding(self, voice_name):
        """
        Retrieves the speaker embedding for a given voice.

        Args:
            voice_name (str): The name of the voice.

        Returns:
            torch.Tensor: The speaker embedding tensor.

        Raises:
            ValueError: If the voice is not available.
        """
        if voice_name not in self.voices:
            raise ValueError(f"Voice '{voice_name}' is not available.")
        index = self.voices[voice_name]
        embedding = torch.tensor(self.embeddings_dataset[index]["xvector"]).unsqueeze(0).to(device)
        return embedding
