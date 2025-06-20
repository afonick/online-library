from celery import Celery
from celery.schedules import crontab
from src.core.config import settings

app = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.celery_tasks",
    ]
)
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    "refresh-and-report-stats-every-day": {
        "task": "src.tasks.celery_tasks.refresh_and_report_stats",
        "schedule": crontab(hour=0, minute=0),
    },
}
