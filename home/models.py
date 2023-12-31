from django.db import models

# Create your models here.

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    timeStamp = models.DateField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.CharField(max_length=100)

    def __str__(self):
        return 'Message from ' + self.name