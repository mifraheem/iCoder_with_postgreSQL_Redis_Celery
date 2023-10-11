# Create your tasks here
from celery import shared_task
from .models import Post

@shared_task
def createBlog(username, title, content):
    try:
        new_post = Post.objects.create(author=username, title=title, content=content)
        new_post.save()
        print("-----------Task done=========")
    except Exception as e:
        print(e )
