# backend/app/utils/message_queue.py

from celery import Celery
from flask import current_app

def make_celery(app):
    """
    Create a Celery object and tie it to the Flask app's config.

    Args:
        app (Flask, optional): The Flask application instance.

    Returns:
        Celery: The configured Celery instance.
    """
    celery = Celery(
        app.import_name,
        broker=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        backend=app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    )
    celery.conf.update(app.config)

    # Subclass Task to ensure that each task runs within the Flask app context
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
