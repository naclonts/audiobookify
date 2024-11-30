# backend/app/controllers/tts_engine.py

import os
from TTS.api import TTS
from .voice_manager import VoiceManager

def generate_speech(text, voice_name, output_path):
    """
    Generates speech audio from text using the specified voice.

    Args:
        text (str): The text to convert to speech.
        voice_name (str): The name of the voice to use.
        output_path (str): The file path to save the generated audio.

    Returns:
        str: The path to the generated audio file.
    """
    try:
        voice_manager = VoiceManager()
        tts_model_path, tts_config_path = voice_manager.get_voice_model(voice_name)

        if not os.path.exists(tts_model_path) or not os.path.exists(tts_config_path):
            raise ValueError(f"Voice model files not found for voice: {voice_name}")

        tts = TTS(model_path=tts_model_path, config_path=tts_config_path)

        # Generate speech and save to output_path
        tts.tts_to_file(text=text, file_path=output_path)

        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to generate speech: {e}")
