from celery import Celery
from app.config.setting import Settings

settings = Settings()

celery_app = Celery(
    "events",
    broker=settings.CELERY_BROKER_URL,
    include=[
        "app.infrastructure.celery.task",
    ]
)

celery_app.conf.timezone = "UTC"

celery_app.conf.beat_schedule = {
    "sync-events-daily": {
        "task": "app.infrastructure.celery.task.sync_events",
        "schedule": 60 * 60 * 24,
    },
}