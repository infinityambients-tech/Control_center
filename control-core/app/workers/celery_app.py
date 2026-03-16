from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery("workers", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Automated sync schedule
celery_app.conf.beat_schedule = {
    "sync-all-projects-every-5-minutes": {
        "task": "app.workers.tasks.sync_projects_task",
        "schedule": crontab(minute=f"*/{settings.SYNC_INTERVAL_MINUTES}"),
    },
}

celery_app.autodiscover_tasks(["app.workers"])
