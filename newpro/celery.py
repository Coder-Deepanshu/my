# newpro/celery.py (create if not exists):
import os
from celery import Celery

# Django settings module set करो
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newpro.settings')

# Celery app create करो
app = Celery('newpro')

# Settings से configuration load करो
app.config_from_object('django.conf:settings', namespace='CELERY')

# All Django apps में tasks auto-discover करो
app.autodiscover_tasks()

# Optional: Task को test के लिए
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')