from flask import current_app
from celery import shared_task
from app.models.task_model import db, Task
from app.controllers import extract_text, clean_text, generate_speech
import os
import logging

logger = logging.getLogger(__name__)

@shared_task(name='process_pdf_task')
def process_pdf_task(task_id):
    """Process a PDF file and convert it to audio."""
    try:
        # Get task from database
        task = Task.query.filter_by(task_id=task_id).first()
        if not task:
            logger.error(f"Task {task_id} not found")
            return False

        # Update task status
        task.status = 'processing'
        db.session.commit()
        logger.info(f"Started processing task {task_id}")

        # Extract text from PDF
        logger.info(f"Extracting text from PDF for task {task_id}")
        raw_text = extract_text(task.file_path)
        logger.info(f"Text extraction completed for task {task_id}")

        # Clean extracted text
        logger.info(f"Cleaning extracted text for task {task_id}")
        cleaned_text = clean_text(raw_text)
        logger.info(f"Text cleaning completed for task {task_id}")

        # Generate speech from cleaned text
        audio_filename = f"{task_id}_audio.wav"
        audio_path = os.path.join(current_app.config['AUDIO_FOLDER'], audio_filename)
        logger.info(f"Generating speech for task {task_id} with voice {task.voice}")
        generate_speech(cleaned_text, task.voice, audio_path)
        logger.info(f"Speech generation completed for task {task_id}")

        # Update task status
        task.audio_path = audio_path
        task.status = 'completed'
        db.session.commit()
        logger.info(f"Task {task_id} completed successfully")

        return True

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {str(e)}")
        if task:
            task.status = 'failed'
            task.error_message = str(e)
            db.session.commit()
        return False
