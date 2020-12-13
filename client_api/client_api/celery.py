import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'client_api.settings')

celery_app = Celery('CLIENT_API', include=['utils.tasks'])
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
