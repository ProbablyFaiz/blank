from celery import Celery, signals

from blanket.db.redis import get_redis_url
from blanket.io.log import safe_init_sentry
from blanket.jobs.schedule import BEAT_SCHEDULE


@signals.celeryd_init.connect
def init_sentry(**_kwargs):
    safe_init_sentry()


def get_celery_app() -> Celery:
    app = Celery("blanket", broker=get_redis_url(), include=["blanket.jobs.tasks"])

    # Configure Celery
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        enable_utc=True,
        worker_concurrency=4,
        beat_schedule=BEAT_SCHEDULE,
    )

    return app


# Create singleton instance
celery_app = get_celery_app()
