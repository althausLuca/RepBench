from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepBenchWeb.settings')
app = Celery('RepBenchWeb')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.event_serializer = 'pickle'
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize']

# Configure the CELERY_IMPORTS setting
app.conf.imports = app.conf.imports + ('RepBenchWeb.tasks',)
