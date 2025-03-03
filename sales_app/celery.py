import os
from celery import Celery

# Set default Django settings module for 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales_app.settings')

app = Celery("sales_app")

# Load configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks from installed Django apps
app.autodiscover_tasks()
