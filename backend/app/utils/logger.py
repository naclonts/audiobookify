# backend/app/utils/logger.py

import logging
import os
from flask import current_app

def setup_logger():
    """
    Sets up the application logger.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if logger is already set up
    if not logger.handlers:
        # Create log directory if it doesn't exist
        log_dir = current_app.config.get('LOG_DIR', 'logs')
        os.makedirs(log_dir, exist_ok=True)

        # File handler
        log_file = os.path.join(log_dir, 'app.log')
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        logger.info("Logger initialized.")
