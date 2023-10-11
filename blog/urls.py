from django.urls import path, include
from .import views

urlpatterns = [
    # API to post a comment
    path('postComment', views.postComment, name="postComment"),
    path('createPost', views.createPost, name='createPost'),
    path('', views.blogHome, name='bloghome'),
    path('<str:slug>', views.blogPost, name='blogpost'),

]
 