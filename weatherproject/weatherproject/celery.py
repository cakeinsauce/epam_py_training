import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherproject.settings")

app = Celery("weatherproject")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "largest_cities_caching": {
        "task": "weather.tasks.cache_cities_forecasts",
        "schedule": 60 * 60,  # every hour
    }
}
