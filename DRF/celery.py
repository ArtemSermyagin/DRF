import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRF.settings")
app = Celery("DRF")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update_rating_themes": {
        "task": "course.tasks.block_inactive_users",
        "schedule": crontab(
            minute='0',
            hour='0',
        ),
    },
}
