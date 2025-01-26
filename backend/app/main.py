import os

from flask import Flask
from flask_cors import CORS

from app.routes import api_routes
from app.utils.logger import setup_logger
from app.utils.message_queue import make_celery
from app.models.task_model import db  # Import the SQLAlchemy instance

def create_app():
    app = Flask(__name__)

    # Load configuration first
    app.config['UPLOAD_FOLDER'] = 'uploads/pdfs'
    app.config['AUDIO_FOLDER'] = 'uploads/audio'
    app.config['LOG_DIR'] = 'logs'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    # Update database configuration for PostgreSQL
    print('DB URL: ',os.getenv('DATABASE_URL'))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        # default local testing URL
        'postgresql://postgres:postgres@localhost:5432/audiobookify'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # Initialize extensions within context
        setup_logger()
        db.init_app(app)

        # Initialize Celery
        celery = make_celery(app)
        app.extensions['celery'] = celery

        # Enable CORS
        CORS(app)

        # Register Blueprints
        app.register_blueprint(api_routes, url_prefix='/api')

        # Create directories
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)
        os.makedirs(app.config['LOG_DIR'], exist_ok=True)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(host='0.0.0.0', port=5000, debug=True)
