# backend/app/controllers/voice_manager.py

import os

class VoiceManager:
    """
    Manages available TTS voices and their corresponding models.
    """

    def __init__(self):
        # Directory where voice models are stored
        self.voices_dir = os.path.join(os.path.dirname(__file__), '..', 'voices')
        self.voices = self.load_available_voices()

    def load_available_voices(self):
        """
        Loads available voices from the voices directory.

        Returns:
            dict: A dictionary mapping voice names to their model and config paths.
        """
        voices = {}
        if not os.path.exists(self.voices_dir):
            os.makedirs(self.voices_dir)

        for voice_name in os.listdir(self.voices_dir):
            voice_path = os.path.join(self.voices_dir, voice_name)
            if os.path.isdir(voice_path):
                model_path = os.path.join(voice_path, 'model.pth')
                config_path = os.path.join(voice_path, 'config.json')
                if os.path.exists(model_path) and os.path.exists(config_path):
                    voices[voice_name] = {
                        'model_path': model_path,
                        'config_path': config_path
                    }
        return voices

    def get_available_voices(self):
        """
        Returns a list of available voice names.

        Returns:
            list: List of voice names.
        """
        return list(self.voices.keys())

    def get_voice_model(self, voice_name):
        """
        Retrieves the model and config paths for a given voice.

        Args:
            voice_name (str): The name of the voice.

        Returns:
            tuple: (model_path, config_path)

        Raises:
            ValueError: If the voice is not available.
        """
        voice = self.voices.get(voice_name)
        if not voice:
            raise ValueError(f"Voice '{voice_name}' is not available.")
        return voice['model_path'], voice['config_path']
