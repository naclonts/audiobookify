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
    task_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    file_path = db.Column(db.String(500), nullable=False)
    audio_path = db.Column(db.String(500), nullable=True)
    voice = db.Column(db.String(100), nullable=False, default='cmu_us_bdl_arctic')
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.task_id} - {self.status} - Voice: {self.voice}>"
