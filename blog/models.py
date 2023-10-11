from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Post (models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=25)
    author = models.CharField(max_length=50)
    content = models.TextField()
    slug = models.CharField(max_length=130)
    views = models.IntegerField(default=0)
    timeStamp = models.DateField(blank=True, auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[0:12] + "..." + " by " + self.user.username