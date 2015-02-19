from django.conf.urls import patterns, url

from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from registration import views

urlpatterns = patterns('',
    # Login / logout /register
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register/$', CreateView.as_view(
            template_name='registration/register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),

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

)