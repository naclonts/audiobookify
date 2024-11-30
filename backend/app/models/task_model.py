# backend/app/models/task_model.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    """
    Represents a task for processing a PDF to audio.
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    pdf_path = db.Column(db.String(200), nullable=False)
    audio_path = db.Column(db.String(200), nullable=True)
    voice = db.Column(db.String(100), nullable=False, default='default_voice')  # New field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.task_id} - {self.status} - Voice: {self.voice}>"
