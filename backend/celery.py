from celery import Celery
from celery.schedules import crontab

app = Celery('backend', broker='redis://localhost:6380/0')


app.conf.update(
    result_backend='redis://localhost:6380/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
app.autodiscover_tasks(['pwa'])


app.conf.beat_schedule = {
    'precache-every-hour': {
        'task': 'pwa.tasks.precache_assets',
        'schedule': crontab(minute=0),
    },
}