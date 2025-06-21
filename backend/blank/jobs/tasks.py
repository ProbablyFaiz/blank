from blank.jobs.celery import celery_app


@celery_app.task
def test_job():
    print("test_job")
