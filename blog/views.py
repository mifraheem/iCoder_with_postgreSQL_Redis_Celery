from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
from django.core.cache import cache
import time
# from iCoder.celery import add
from celery.result import AsyncResult
from . tasks import createBlog

# Create your views here.
def blogHome(request):
    # result = add.delay(10,20)
    # print(f"Result 1: {result}")
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    start = time.time()
    if cache.get(slug):
        print("Data from Cache.===")
        print(cache.ttl(slug))
        post = cache.get(slug)
        comments = cache.get(f'comments_{post.pk}') ## not good practice
        replies = cache.get(f'replies_{post.pk}') 
    else:
        post = Post.objects.filter(slug=slug).first()
        comments = BlogComment.objects.filter(post=post, parent = None)
        replies = BlogComment.objects.filter(post=post).exclude(parent=None)
        cache.set(slug, post, 20)
        cache.set(f'comments_{post.pk}', comments, 20)
        cache.set(f'replies_{post.pk}', replies, 20)

        print("Data from Database.")
    post.views = post.views + 1
    post.save()
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post':post, 'comments': comments, 'user': request.user, 'replyDict':replyDict}
    print(time.time() - start)
    return render(request, 'blog/blogPost.html',context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno = postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user = user, post=post)
            messages.success(request, 'Your comment has bees posted successfully.')
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user = user, post=post, parent=parent)
            messages.success(request, 'Your reply has bees posted successfully.')
        comment.save()
    return redirect(f"/blog/{post.slug}")



def createPost(request):
    
    if request.method=='POST':
        titel = request.POST['title']
        content = request.POST['content']
        # newBLog = Post.objects.create(author = request.user.first_name, title=titel, content=content, slug=time.time())
        print("Sharing task=========")
        createBlog.delay(request.user.first_name, titel, content)
        print("Task Shared===========")

    return render(request, 'blog/createBlog.html')