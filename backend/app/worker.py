# backend/app/celery_worker.py

from app.main import create_app
from app.utils.message_queue import make_celery

app = create_app()
celery = make_celery(app)

if __name__ == '__main__':
    celery.start()
