from celery import Celery

celery_app = Celery("tasks", broker="pyamqp://guest@localhost//")


@celery_app.task
def add():
    return 7


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, add, name="add every 10", expires=30)
