# backend/app/controllers/__init__.py

from .pdf_processor import extract_text
from .text_cleaner import clean_text
from .tts_engine import generate_speech
from .voice_manager import VoiceManager

__all__ = [
    'extract_text',
    'clean_text',
    'generate_speech',
    'VoiceManager'
]
