from django.db import models
from django.contrib.auth.models import User

class InstagramAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fb_user_id = models.CharField(max_length=100)
    access_token = models.TextField()
    token_expires = models.DateTimeField()

class ScheduledPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField()
    caption = models.TextField(blank=True)
    scheduled_time = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
