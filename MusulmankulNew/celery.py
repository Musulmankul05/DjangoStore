import os

from celery import Celery

from MusulmankulNew import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusulmankulNew.settings')

app = Celery('MusulmankulNew')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
