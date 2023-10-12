# Create your tasks here
from celery import shared_task
from .models import Post
from time import sleep
@shared_task(name="Async Blog Uploading")
def createBlog(username, title, content):
    try:
        # sleep(5)
        new_post = Post.objects.create(author=username, title=title, content=content)
        new_post.save()
        print("-----------Task done=========")
    except Exception as e:
        print(e )


@shared_task
def clear_session_cache(id):
    print(f"Session cache cleared: {id}")
    return id