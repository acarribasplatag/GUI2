from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',

    # ex: localhost:8000/
    url(r'^$', views.categories, name='home'),
    
    # ex: localhost:8000/index.html
    url(r'^index.html$', views.categories, name='home'),
    
    # ex: localhost:8000/topic_select/   (category selection screen)
    url(r'^topic_select/$', views.topic_select, name='topic_select'),
    
    # ex: localhost:8000/1/2 (first category, second question)
    url(r'^(?P<category_id>\d+)/(?P<question_id>\d+)/$', 
        views.question, name='question'),
    
    # ex: localhost:8000/categories/
    url(r'^categories/$', views.get_all_categories, name='get_all_categories'),
    
    # ex: localhost:8000/about/
    url(r'^about/$', views.about, name='about'),
    
    # ex: localhost:8000/contact/
     url(r'^contact/', include('polls/contact_form.urls')),
    
    # ex:localhost:8000/myAccount/
    url(r'^myAccount/$', views.myAccount, name='dashboard'),
    
    # ex:localhost:8000/myAccount/password_change
    url(r'^myAccount/password_change/$',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect' : '/myAccount/password_change/done/', 
        'template_name': 'polls/change_password/password_change_form.html'},
        name="password_change"),
        
    # ex:localhost:8000/myAccount/password_change/done
    url(r'^myAccount/password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'polls/change_password/password_change_done.html'}),
        
    # ex:localhost:8000/create_topic
    url(r'^create_topic/$', views.create_topic, name='create_topic'),
      
)
