from celery.schedules import crontab

BEAT_SCHEDULE = {
    "healthy-job": {
        "task": "blanket.jobs.tasks.healthy_job",
        "schedule": crontab(minute="*/1"),
    },
}
