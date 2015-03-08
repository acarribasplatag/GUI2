import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    avatar = models.ImageField()
    aboutMe = models.TextField()
    interests = models.TextField()
    def __unicode__(self):              # __str__ on Python 3
        return self.user.username
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    # Other fields associated with a user.