from blanket.jobs.celery import celery_app


@celery_app.task
def healthy_job():
    print("healthy_job")
