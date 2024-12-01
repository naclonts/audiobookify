# backend/app/controllers/tasks.py

from app.utils.message_queue import make_celery
from app.controllers import extract_text, clean_text, generate_speech
from app.models.task_model import db, Task
from flask import current_app
import os

celery = make_celery()

@celery.task()
def process_pdf_task(task_id):
    try:
        task = Task.query.filter_by(task_id=task_id).first()
        if not task:
            current_app.logger.error(f"Task {task_id} not found.")
            return

        task.status = 'processing'
        db.session.commit()

        # Extract text from PDF
        raw_text = extract_text(task.pdf_path)

        # Clean the extracted text
        cleaned_text = clean_text(raw_text)

        # Generate speech audio using the selected voice
        audio_filename = f"{task_id}_audio.wav"
        audio_path = os.path.join(current_app.config['AUDIO_FOLDER'], audio_filename)
        generate_speech(cleaned_text, task.voice, audio_path)

        # Update task with audio path and status
        task.audio_path = audio_path
        task.status = 'completed'
        db.session.commit()

        current_app.logger.info(f"Task {task_id} completed successfully.")

    except Exception as e:
        if task:
            task.status = 'failed'
            db.session.commit()
        current_app.logger.error(f"Error processing task {task_id}: {e}")
