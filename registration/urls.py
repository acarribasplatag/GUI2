from django.conf.urls import patterns, url

from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from registration import views

urlpatterns = patterns('',
    # Login / logout /register
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url('^register/', CreateView.as_view(
            template_name='registration/register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    
)