# Create your tasks here
from celery import shared_task
from .models import Post
from time import sleep
from time import time
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


@shared_task(name="Async Blog Uploading")
def createBlog(username, title, content):
    try:
        # sleep(5)
        new_post = Post.objects.create(
            author=username, title=title, content=content, slug=time())
        new_post.save()
        print("-----------Task done=========")
    except Exception as e:
        print(e)


@shared_task
def clear_session_cache(id):
    print(f"Session cache cleared: {id}")
    return id


@shared_task
def clear_redis_cache(key):
    print(f"Redis cache cleared: {key}")
    return key


@shared_task
def check_django_celery_beat_in_code(key):
    print(f"This task is scheduled in code: {key}")
    return key


schedule, created = IntervalSchedule.objects.get_or_create(
    every=20,
    period=IntervalSchedule.SECONDS,
    )

PeriodicTask.objects.get_or_create(
    name='Testing DJango-celery-beat task through program',
    task='blog.tasks.check_django_celery_beat_in_code',
    interval=schedule,
    args=json.dumps(['Hello']),
)
