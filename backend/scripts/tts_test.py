import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.controllers.tts_engine import generate_speech

def main():
    sample_text = "This is a sample text to test the text-to-speech functionality."
    voice = "cmu_us_bdl_arctic"  # Specify the voice you want to use
    output_file = "output_audio.wav"

    try:
        generate_speech(sample_text, voice, output_file)
        print(f"Speech generated successfully and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
