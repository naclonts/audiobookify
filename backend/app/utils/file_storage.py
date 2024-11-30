# backend/app/utils/file_storage.py

import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_file(file, folder):
    """
    Saves an uploaded file to the specified folder.

    Args:
        file (werkzeug.datastructures.FileStorage): The uploaded file.
        folder (str): The folder to save the file ('pdfs' or 'audios').

    Returns:
        str: The path to the saved file.
    """
    try:
        filename = secure_filename(file.filename)
        # Generate a unique filename to prevent collisions
        unique_filename = f"{current_app.config.get('UNIQUE_PREFIX', '')}_{filename}"
        save_path = os.path.join(current_app.config.get(f'{folder.upper()}_FOLDER'), unique_filename)
        file.save(save_path)
        current_app.logger.info(f"File saved to {save_path}")
        return save_path
    except Exception as e:
        current_app.logger.error(f"Error saving file: {e}")
        raise

def get_file_path(filename, folder):
    """
    Retrieves the full file path for a given filename and folder.

    Args:
        filename (str): The name of the file.
        folder (str): The folder where the file is stored ('pdfs' or 'audios').

    Returns:
        str: The full path to the file.
    """
    try:
        file_path = os.path.join(current_app.config.get(f'{folder.upper()}_FOLDER'), filename)
        if not os.path.exists(file_path):
            current_app.logger.warning(f"File not found: {file_path}")
            return None
        return file_path
    except Exception as e:
        current_app.logger.error(f"Error retrieving file path: {e}")
        raise