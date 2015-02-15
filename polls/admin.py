from django.contrib import admin
from polls.models import Question, Category, Choice, Comment


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['category_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Category, CategoryAdmin)

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['question_text']}),
        ('Date information',    {'fields': ['pub_date']}),
        ('frozen',              {'fields': ['frozen']}),
        ('Belongs to User',     {'fields': ['user']}),
        ('Belongs to Category', {'fields': ['category']}),
    ]

admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['choice_text']}),
        ('Date information', {'fields': ['pub_date']}),
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