import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    category_text = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    def __str__(self):              # __unicode__ on Python 2
        return self.category_text
    def __unicode__(self):              # __unicode__ on Python 2
        return unicode(self.category_text)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    def __str__(self):              # __unicode__ on Python 2
        return self.question_text
    def __unicode__(self):              # __unicode__ on Python 2
        return unicode(self.question_text)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question) # belongs to a question
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text
    def __unicode__(self):              # __unicode__ on Python 2
        return unicode(self.choice_text)
        
class Comment(models.Model):
    choice = models.ForeignKey(Choice) # belongs to a choice
    comment_text = models.CharField(max_length=500)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    def __str__(self):              # __unicode__ on Python 2
        return self.comment_text
           
class CommentOnComment(models.Model):
    comment = models.ForeignKey(Comment) # belongs to a choice
    comment_text = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    likes = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
        return self.comment_text