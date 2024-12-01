# backend/app/controllers/text_cleaner.py

import re
import unicodedata

def normalize_text(text):
    """
    Normalize special characters in the text to ensure consistent processing.
    """
    # Unicode Normalization
    text = unicodedata.normalize('NFKC', text)

    # Define a mapping of special characters to their replacements using regex patterns
    replacements = {
        r'[‘’‚‛]': "'",
        r'[“”„‟]': '"',
        r'\s[-—―–−]\s': ', ',
        r'…': '...',
        r'•': '-',
        r'[‹›«»]': '"',
        r'[-—―−–-]': ' ',
    }

    # Apply the replacements
    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)

    # Replace non-ASCII characters with a space
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove extra whitespace and trim
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def split_text(text, max_length=598):
    """
    Split the text into chunks where each chunk contains multiple sentences
    without exceeding the max_length.
    """
    # Normalize the text
    text = normalize_text(text)

    # Split the text into sentences
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
                    if len(word_chunk) + len(word) + 1 > max_length:
                        if word_chunk:
                            chunks.append(word_chunk + ' ')
                        word_chunk = word
                    else:
                        word_chunk += (' ' if word_chunk else '') + word

                if word_chunk:
                    if not word_chunk.endswith(('.', '!', '?')):
                        word_chunk += '.'
                    current_chunk = word_chunk

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
