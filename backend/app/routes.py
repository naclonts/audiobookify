# backend/app/routes.py

from flask import Blueprint, request, jsonify, send_from_directory, current_app
import os
import uuid

from app.models.task_model import db, Task
from app.utils.file_storage import save_file
from app.controllers.tasks import process_pdf_task

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type. Please upload a PDF.'}), 400

    if 'voice' not in request.form:
        return jsonify({'error': 'No voice selected.'}), 400

    selected_voice = request.form['voice']

    try:
        # Generate a unique task ID
        task_id = str(uuid.uuid4())

        # Save the uploaded PDF with task_id as prefix
        upload_path = save_file(file, 'pdfs', unique_prefix=task_id)

        current_app.logger.info(f"PDF uploaded and saved to {upload_path}")

        # Create a new Task entry in the database
        task = Task(
            task_id=task_id,
            status='pending',
            pdf_path=upload_path,
            audio_path=None,
            voice=selected_voice
        )
        db.session.add(task)
        db.session.commit()

        current_app.logger.info(f"Task {task_id} created with status 'pending' and voice '{selected_voice}'")

        # Send the task to Celery for processing
        process_pdf_task.delay(task_id)

        return jsonify({'task_id': task_id, 'status': 'pending'}), 202

    except Exception as e:
        current_app.logger.error(f"Error during PDF upload: {e}")
        return jsonify({'error': 'Failed to upload and process the PDF.'}), 500

@api_routes.route('/voices', methods=['GET'])
def get_voices():
    try:
        from app.controllers.voice_manager import VoiceManager
        voice_manager = VoiceManager()
        available_voices = voice_manager.get_available_voices()
        return jsonify({'voices': available_voices}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching voices: {e}")
        return jsonify({'error': 'Failed to retrieve voices.'}), 500

@api_routes.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    try:
        task = Task.query.filter_by(task_id=task_id).first()

        if not task:
            return jsonify({'error': 'Invalid task ID.'}), 404

        return jsonify({'task_id': task.task_id, 'status': task.status}), 200

    except Exception as e:
        current_app.logger.error(f"Error checking status for task {task_id}: {e}")
        return jsonify({'error': 'Failed to retrieve task status.'}), 500

@api_routes.route('/download/<task_id>', methods=['GET'])
def download_audio(task_id):
    try:
        task = Task.query.filter_by(task_id=task_id).first()

        if not task:
            return jsonify({'error': 'Invalid task ID.'}), 404

        if task.status != 'completed' or not task.audio_path:
            return jsonify({'error': 'Audio not available yet.'}), 400

        directory = os.path.dirname(task.audio_path)
        filename = os.path.basename(task.audio_path)
        return send_from_directory(directory, filename, as_attachment=True)

    except Exception as e:
        current_app.logger.error(f"Error downloading audio for task {task_id}: {e}")
        return jsonify({'error': 'Failed to download audio.'}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'
