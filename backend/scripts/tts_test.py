from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import numpy as np
import re
import unicodedata

# Check if GPU is available and set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load processor and models
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

# Load xvector containing speaker's voice characteristics from a dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0).to(device)


def normalize_text(text):
    """
    Normalize special characters in the text to ensure consistent processing.
    - Normalize Unicode characters.
    - Replace smart quotes and apostrophes with standard ones.
    - Replace different types of dashes with standard hyphen.
    - Replace ellipses with standard periods.
    - Remove or replace unwanted characters.
    """
    # 1. Unicode Normalization: Convert characters to their canonical forms
    text = unicodedata.normalize('NFKC', text)

    # 2. Define a mapping of special characters to their replacements using regex patterns
    replacements = {
        # Smart single quotes and apostrophes to straight apostrophe
        r'[‘’‚‛]': "'",
        # Smart double quotes to straight double quote
        r'[“”„‟]': '"',
        # Replace specific dash patterns with a comma and space
        r'\s[-—―–−]\s': ', ',
        # Ellipsis to three periods
        r'…': '...',
        # Bullet points to hyphen
        r'•': '-',
        # Guillemets to straight double quotes
        r'[‹›«»]': '"',
        # Various dashes and hyphens to space
        r'[-—―−–-]': ' ',
    }


    # 3. Apply the replacements
    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)

    # 4. Replace non-ASCII characters with a space\
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # 5. Remove extra whitespace (multiple spaces, tabs, newlines) and trim
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# Simplified and enhanced split_text function
def split_text(text, max_length=598):
    """
    Split the text into chunks where each chunk contains multiple sentences
    without exceeding the max_length. If a sentence exceeds max_length,
    it is split into smaller parts based on words.
    """
    # Normalize the text to handle special characters
    text = normalize_text(text)

    # Split the text into sentences using regex to handle various punctuation
    # This regex splits on '.', '!', or '?' followed by a space or end of string
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text)

    chunks = []
    current_chunk = ''

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Ensure the sentence ends with appropriate punctuation
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'

        # Check if adding the sentence exceeds the max_length
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += (' ' if current_chunk else '') + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk + ' ')
                current_chunk = ''

            if len(sentence) <= max_length:
                current_chunk = sentence
            else:
                # Split the long sentence into words
                words = sentence.split()
                word_chunk = ''

                for word in words:
                    # Check if adding the next word exceeds the max_length
                    if len(word_chunk) + len(word) + 1 > max_length:
                        if word_chunk:
                            chunks.append(word_chunk + ' ')
                        word_chunk = word
                    else:
                        word_chunk += (' ' if word_chunk else '') + word

                if word_chunk:
                    # Add appropriate punctuation to the last word chunk
                    if not word_chunk.endswith(('.', '!', '?')):
                        word_chunk += '.'
                    current_chunk = word_chunk

    # Append any remaining text in current_chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Function to process a batch of text and generate audio
def generate_audio(texts, output_file="output.wav"):
    combined_audio = []
    samplerate = 16000  # Hertz
    silence = np.zeros(int(0.5 * samplerate), dtype=np.float32)

    for i, text in enumerate(texts):
        print(f"Processing chunk: {text}")
        inputs = processor(text=text, return_tensors="pt").to(device)
        with torch.no_grad():
            speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        combined_audio.append(speech.cpu().numpy())

        # add a breif pause between chunks / sentences
        if i < len(texts) - 1:
          combined_audio.append(silence)

    # Concatenate all audio chunks
    final_audio = np.concatenate(combined_audio)

    # Save the combined audio to a file
    sf.write(output_file, final_audio, samplerate=16000)
    print(f"Audio saved to {output_file}")

# Example large text
large_text = """
Motivated by the success of T5 (Text-To-Text Transfer Transformer) in pre-trained natural language processing models, we propose a unified-modal SpeechT5 framework that explores the encoder-decoder pre-training for self-supervised speech/text representation learning. The SpeechT5 framework consists of a shared encoder-decoder network and six modal-specific (speech/text) pre/post-nets. After preprocessing the input speech/text through the pre-nets, the shared encoder-decoder network models the sequence-to-sequence transformation, and then the post-nets generate the output in the speech/text modality based on the output of the decoder.
"""

# Split the text into chunks
text_chunks = split_text(large_text, max_length=200)

# Process the chunks in batches and save the output audio
generate_audio(text_chunks, output_file="speech.wav")
