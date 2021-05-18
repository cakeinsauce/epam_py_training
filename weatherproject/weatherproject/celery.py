import os
from datetime import datetime

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherproject.settings")

app = Celery("weatherproject")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

now = datetime.now()

# Cron strings for scheduler with offset.

cron_minute = str(now.minute + 1)
cron_hour = str(now.hour)
cron_day = str(now.day)
cron_month = str(now.month)

app.conf.beat_schedule = {
    "initial_largest_cities_caching": {
        "task": "weather.tasks.save_cities_forecasts",
        "schedule": crontab(
            minute=cron_minute,
            hour=cron_hour,
            day_of_month=cron_day,
            month_of_year=cron_month,
        ),
    },
    "largest_cities_caching": {
        "task": "weather.tasks.save_cities_forecasts",
        "schedule": 60 * 60,  # every hour
    },
}
