from django.contrib import admin
from polls.models import Poll, Category, Choice, Comment, Vote


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['category_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Category, CategoryAdmin)

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['poll_text']}),
        ('Date information',    {'fields': ['pub_date']}),
        ('frozen',              {'fields': ['frozen']}),
        ('Belongs to User',     {'fields': ['user']}),
        ('Belongs to Category', {'fields': ['category']}),
    ]

admin.site.register(Poll, PollAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['choice_text']}),
        ('Date information',    {'fields': ['pub_date']}),
        ('Votes',               {'fields': ['votes']}),
        ('Belongs to User',     {'fields': ['user']}),
        ('Belongs to Poll', {'fields': ['poll']}),
    ]

admin.site.register(Choice, ChoiceAdmin)

class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['comment_text']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Blongs to choice', {'fields': ['choice']}),
        ('likes',            {'fields': ['likes']}),
        ('Belongs to User',  {'fields': ['user']}),
    ]

admin.site.register(Comment, CommentAdmin)

class VoteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date information', {'fields': ['pub_date']}),
        ('Belongs to Poll',  {'fields': ['poll']}),
        ('Belongs to Choice',  {'fields': ['choice']}),
        ('Belongs to User',  {'fields': ['user']}),
    ]

admin.site.register(Vote, VoteAdmin)