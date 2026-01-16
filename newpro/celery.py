# celery.py me
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newpro.settings')

app = Celery('newpro')

# Windows ke liye important settings
app.conf.update(
    worker_pool_restarts=True,
    worker_max_tasks_per_child=1,  # Windows ke liye important
    broker_connection_retry_on_startup=True,
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Windows compatibility ke liye
if os.name == 'nt':
    app.conf.update(
        worker_pool='solo',  # Windows pe 'solo' pool use karein
        worker_concurrency=1,
    )