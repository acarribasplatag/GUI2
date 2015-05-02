import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import default

# This is the Category object, polls are seperated into categories.
class Category(models.Model):
    category_text = models.CharField(max_length=50) # Categories Titles
    pub_date = models.DateTimeField('date published') # Date the category was created
    image = models.FileField(upload_to='category/', null=True) # This is the image used on the caroesel.
    def __unicode__(self):              # __str__ on Python 3
        return self.category_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

# This is the poll object.
class Poll(models.Model):
    poll_text = models.CharField(max_length=200) # The title or question the poll is asking.
    category = models.ForeignKey(Category) # A poll belongs to a category.
    user = models.ForeignKey(User) # The poll keeps track of which user created it.
    frozen = models.BooleanField(default=False) # If it is frozen it will not accept votes.
    def __unicode__(self):               # __str__ on Python 3
        return self.poll_text
    # This method of a poll will tell us if it was published recently. 
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

# This is a choice object.
class Choice(models.Model):
    choice_text = models.CharField(max_length=200) # The choice's text.
    poll = models.ForeignKey(Poll) # The poll that it belongs to.
    votes = models.IntegerField(default=0) # The votes that the choice has.
    user = models.ForeignKey(User) # The user that created the choice.
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.choice_text


class Comment(models.Model):
    comment_text = models.CharField(max_length=500) # The text of a comment.
    choice = models.ForeignKey(Choice) # Comments belong to choices.
    likes = models.IntegerField(default=0) # How many likes a comment has.
    user = models.ForeignKey(User) # The user that created the comment.
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.comment_text

class Vote(models.Model):
    old = models.BooleanField(default=False) # Users can change their vote, when they do a vote becomes "old".
    poll = models.ForeignKey(Poll) # We keep track of what poll the vote was on.
    choice = models.ForeignKey(Choice) # What choice the vote was for.
    user = models.ForeignKey(User) # Who the vote belongs too.
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.choice.choice_text

# Negative votes are for when a user changes their vote. We needed a way
# to show on the timeline that the user had voted for a choice but then changed it
# ie. a user votes for "yes", then changes to "no", we keep the "yes" vote and then
# add a negative vote to "yes" so that the timeline will show go up and then down when they change their vote
class NegativeVote(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):               # __str__ on Python 3
        return self.choice.choice_text

# This is the Like object.
class Like(models.Model):
    user = models.ForeignKey(User) # Belongs to a user.
    comment = models.ForeignKey(Comment) #Is assosiated with a comment.
    pub_date = models.DateTimeField('date published') # We keep track of when the like was made.
    def __unicode__(self):               # __str__ on Python 3
        return self.comment.comment_text

# This is the object created when a user uses the "contact us" page.
# We can see these when we log into the admin page.
class Feedback(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=5000)
    def __unicode__(self):               # __str__ on Python 3
        return self.comment


