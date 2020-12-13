from celery import Celery

celery_app = Celery('MLAPI', include=['core.tasks'])
celery_app.config_from_object('core.config', namespace='CELERY')
