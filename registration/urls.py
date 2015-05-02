# This file contains the urls for the site and the views loaded on navigation to those urls

from django.conf.urls import patterns, url, include

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

    url(r'^password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/password_reset/done/'},
        name="password_reset"),
    (r'^password_reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
     'django.contrib.auth.views.password_reset_confirm',
     {'post_reset_redirect' : '/reset/done/'}),
    (r'^reset/done/$', 
        'django.contrib.auth.views.password_reset_complete'),

    # ex:localhost:8000/myAccount/password_change/done
    url(r'^myAccount/password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'registration/password_change_done.html'}),
    url(r'^user/(?P<user_id>\d+)/$', views.public_profile, name='public_profile'),
    url(r'^user/edit/(?P<user_id>\d+)/$', views.public_profile_edit, name='public_profile_edit'),
    url(r'^user/(?P<user_id>\d+)/upload_pic/$', views.upload_pic, name='upload-profile-pic'),
    url(r'^view_pdf_summary/(?P<poll_id>\d+)/$', views.view_pdf_report, name="view-pdf-report"),
    url(r'^user/(?P<user_id>\d+)/close/$', views.close_account, name='close-account'),

)