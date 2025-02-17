from app.celery import celery
from celery.schedules import crontab

celery.conf.beat_schedule = {
    "notify_users": {
        "task": "app.celery.notifications.notify_users_about_subscription",
        "schedule": crontab(hour=10, minute=0),
    }
}
