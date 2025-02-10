from celery.schedules import crontab


celery.conf.beat_schedule = {
    "notify_users": {
        "task": "tasks.notify_users_about_subscription",
        "schedule": crontab(hour=10, minute=0),
    }
}
