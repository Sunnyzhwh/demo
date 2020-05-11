import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tantan.settings')


celery_app = Celery('tantan')
celery_app.config_from_object('worker.config')
celery_app.autodiscover_tasks()


def call_by_worker(func):
    '''将任务在celery中异步执行'''
    task = celery_app.task(func)
    return task.delay
