import torch
import numpy as np
import soundfile as sf
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from app.controllers.text_cleaner import split_text
from app.controllers.voice_manager import VoiceManager

# Check if GPU is available and set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load processor and models
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

voice_manager = VoiceManager()

def generate_speech(text: str, voice_name: str, output_path: str) -> str:
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
        # Get speaker embedding for the selected voice
        speaker_embedding = voice_manager.get_voice_embedding(voice_name)

        # Normalize and split text
        text_chunks = split_text(text, max_length=200)

        combined_audio = []
        samplerate = 16000  # Hertz
        silence = np.zeros(int(0.5 * samplerate), dtype=np.float32)

        for i, chunk in enumerate(text_chunks):
            inputs = processor(text=chunk, return_tensors="pt").to(device)
            with torch.no_grad():
                speech = model.generate_speech(inputs["input_ids"], speaker_embedding, vocoder=vocoder)
            combined_audio.append(speech.cpu().numpy())
            # Add a brief pause between chunks
            if i < len(text_chunks) - 1:
                combined_audio.append(silence)

        # Concatenate all audio chunks
        final_audio = np.concatenate(combined_audio)

        # Save the combined audio to a file
        sf.write(output_path, final_audio, samplerate=samplerate)
        return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to generate speech: {e}")
