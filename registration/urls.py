from django.conf.urls import patterns, url

from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import PollPortalUserCreationForm
from registration import views

urlpatterns = patterns('',
    # Login / logout /register
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register/$', views.register_user, name='register_user'),

    # ex:localhost:8000/myAccount/
    url(r'^myAccount/$', views.myAccount, name='dashboard'),

    # ex:localhost:8000/myAccount/password_change
    url(r'^myAccount/password_change/$',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect' : '/myAccount/password_change/done/',
        'template_name': 'registration/password_change_form.html'},
        name="password_change"),

    # ex:localhost:8000/myAccount/password_change/done
    url(r'^myAccount/password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'registration/password_change_done.html'}),
    url(r'^user/(?P<user_id>\d+)/', views.public_profile, name='public_profile'),
    url(r'^user/edit/(?P<user_id>\d+)/', views.public_profile_edit, name='public_profile_edit'),
    url(r'^user/(?P<user_id>\d+)/upload_pic/', views.upload_pic, name='upload-profile-pic'),

)