import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    # This field is required. User Profile belongs to a user
    user = models.OneToOneField(User)
    avatar = models.FileField(upload_to='profile/', null=True)
    aboutMe = models.TextField(null=True, blank=true)
    interests = models.TextField(null=True, blank=true)
    def __unicode__(self):              # __str__ on Python 3
        return self.user.username