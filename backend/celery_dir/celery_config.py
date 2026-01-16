from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "project",
    broker="redis://localhost:6379/0", #redis
)

celery_app.conf.beat_schedule = {
    "expire-orders-every-minute": {
        "task": "celery_dir.tasks.expire_orders",
        "schedule": crontab(minute="*/1"),
    }
}

celery_app.conf.timezone = "UTC"