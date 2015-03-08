from django.contrib import admin
from registration.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Avatar',              {'fields': ['avatar']}),
        ('Belongs to User',     {'fields': ['user']}),
        ('About User:', {'fields': ['aboutMe']}),
        ('Interests of User:', {'fields': ['interests']}),
    ]

admin.site.register(UserProfile, UserProfileAdmin)