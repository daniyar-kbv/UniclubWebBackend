import os
from celery import Celery


if not ("DJANGO_SETTINGS_MODULE" in os.environ):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uniclub.settings")

app = Celery("uniclub")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
