from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',

    # ex: localhost:8000/
    url(r'^$', views.home, name='home'),

    # ex: localhost:8000/topic_select/   (category selection screen)
    url(r'^polls/$', views.polls, name='polls'),

    # ex: localhost:8000/1/2 (first category, second poll)
    url(r'^(?P<category_id>\d+)/(?P<poll_id>\d+)/$',
        views.poll, name='question'),

    url(r'^get_chart/(?P<poll_id>\d+)/$',
        views.get_poll_chart, name='get_chart'),

    # ex: localhost:8000/categories/
    url(r'^categories/$', views.get_all_categories, name='get_all_categories'),

    # ex: localhost:8000/about/
    url(r'^about/$', views.about, name='about'),

    # ex: localhost:8000/contact/
    url(r'^contact/', include('contact_form.urls')),

    # ex: localhost:8000/freeze_voting/(category_id)/(poll_id)
    url(r'^freeze_voting/(?P<category_id>\d+)/(?P<poll_id>\d+)/$',
        views.freeze_voting, name='freeze_voting'),

    # ex: localhost:8000/delete_poll/(category_id)/poll_id/
    url(r'^delete_poll/(?P<category_id>\d+)/(?P<poll_id>\d+)/$',
        views.delete_poll, name='delete_poll'),

    # ex:localhost:8000/create_question
    url(r'^create_question/$', views.create_question, name='create_topic'),
    
    url(r'^vote/$',
        views.vote, name='vote'),
                       
    url(r'^new_comment/$',
        views.writecomment, name='writecomment'),

)
