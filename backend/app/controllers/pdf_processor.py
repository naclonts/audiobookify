# backend/app/controllers/pdf_processor.py

from pdfminer.high_level import extract_text as pdf_extract_text

def extract_text(file_path):
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The file path to the PDF.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        text = pdf_extract_text(file_path)
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")
