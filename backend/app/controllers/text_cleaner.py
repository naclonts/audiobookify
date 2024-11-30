# backend/app/controllers/text_cleaner.py

import re

def clean_text(raw_text):
    """
    Cleans the extracted text by removing headers/footers,
    fixing hyphenated words, and general text cleanup.

    Args:
        raw_text (str): The raw text extracted from the PDF.

    Returns:
        str: The cleaned text.
    """
    try:
        # Remove headers and footers using regex
        # This is a simplistic approach; may need adjustment based on PDF structure
        lines = raw_text.split('\n')
        cleaned_lines = []
        header_footer_pattern = re.compile(r'^\s*(Page\s+\d+|Chapter\s+\d+|.*)\s*$')  # Example patterns

        for line in lines:
            if not header_footer_pattern.match(line):
                cleaned_lines.append(line)

        cleaned_text = '\n'.join(cleaned_lines)

        # Fix hyphenated words at line breaks
        cleaned_text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', cleaned_text)

        # Replace multiple newlines with a single newline
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)

        # Additional cleanup can be added here (e.g., removing extra spaces)
        cleaned_text = re.sub(r' +', ' ', cleaned_text)

        return cleaned_text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to clean text: {e}")
