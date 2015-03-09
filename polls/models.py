import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    category_text = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):              # __str__ on Python 3
        return self.category_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Poll(models.Model):
    poll_text = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    frozen = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.poll_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll) # belongs to a poll
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.choice_text


class Comment(models.Model):
    comment_text = models.CharField(max_length=500)
    choice = models.ForeignKey(Choice) # belongs to a choice
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.comment_text

class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.choice.choice_text
    
class Like(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.comment.comment_text

class Feedback(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=5000)
    def __unicode__(self):               # __str__ on Python 3
        return self.comment


