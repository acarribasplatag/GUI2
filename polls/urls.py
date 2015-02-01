from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    #ex: localhost:8000/
    url(r'^$', views.categories, name='categories'),
    #ex: localhost:8000/1   (first category)
    url(r'^(?P<category_id>\d+)/$', views.questions, name='questions'),
    #ex: localhost:8000/1/2 (first category, second question)
    url(r'^(?P<category_id>\d+)/(?P<question_id>\d+)/$', views.question, name='question'),
)