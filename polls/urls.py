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

    url(r'^get_chart/(?P<question_id>\d+)/$',
        views.get_question_chart, name='get_chart'),

    # ex: localhost:8000/categories/
    url(r'^categories/$', views.get_all_categories, name='get_all_categories'),

    # ex: localhost:8000/about/
    url(r'^about/$', views.about, name='about'),

    # ex: localhost:8000/contact/
    url(r'^contact/', include('contact_form.urls')),

    url(r'^myAccount/freeze_voting/(?P<question_id>\d+)/$',
        views.freezeVoting, name='freeze_voting'),
    url(r'^myAccount/delete_topic/(?P<question_id>\d+)/$',
        views.delete_new, name='delete_topic'),

    # ex:localhost:8000/create_topic
    url(r'^create_topic/$', views.create_topic, name='create_topic'),

)
