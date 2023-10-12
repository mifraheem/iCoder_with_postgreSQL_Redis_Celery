import os
from celery import Celery
from time import sleep
from datetime import timedelta
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iCoder.settings')

app = Celery('iCoder')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# @app.task(name="Addition Task")
# def add(x,y):
#     print(f"Task Received to add {x} and {y}")
#     sleep(5)
#     return x+y


# schedule tasks to run automatically (METHOD #02)
# app.conf.beat_schedule = {    
#     'every-10-seconds-method-02': {
#         'task': 'blog.tasks.clear_session_cache',
#         'schedule': 10,
#         'args': ('1111', )
#     }
#     # add more tasks here. 
# }

# METHOD #02 with timedelta and crontab
app.conf.beat_schedule = {    
    'every-10-seconds-method-02': {
        'task': 'blog.tasks.clear_session_cache',
        # 'schedule': timedelta(seconds=10),
        # 'schedule': crontab(minute='*/1'),
        'schedule': crontab(hour=9, minute=8),
        
        'args': ('1111', )
    }
    # add more tasks here. 
}




@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
