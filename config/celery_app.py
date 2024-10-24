import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("midnight_times")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
   "check_due_date_and_send_email": {
      "task": "midnight_times.users.tasks.clear_results",
      "schedule": crontab(minute=0, hour=0),
   },

}
