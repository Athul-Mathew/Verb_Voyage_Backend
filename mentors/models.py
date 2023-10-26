from django.db import models
from django.http import JsonResponse
from Accounts.models import *

# Create your models here.
class Mentor(models.Model):
    
    name = models.CharField(max_length=255)
    user =models.OneToOneField(UserAccount, on_delete=models.CASCADE ,null=True)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    qualifications = models.TextField()
    education = models.TextField()
    image = models.ImageField(upload_to='mentor_images/',null=True)
    phoneNumber = models.CharField(max_length=20)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.name 


class Playlist(models.Model):
    title = models.CharField(max_length=255)
    premium = models.BooleanField(default=False)
   
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
 # Added user field

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title
 

# models.py



class Notification(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    

