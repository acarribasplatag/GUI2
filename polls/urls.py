from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',

    # ex: localhost:8000/
    url(r'^$', views.home, name='home'),

    # ex: localhost:8000/polls/   (category selection screen)
    url(r'^polls/$', views.polls, name='polls'),

    #ex: localhost:8000/create_poll/
    url(r'^create_poll/$', views.create_poll, name='create_poll'),


    # ex: localhost:8000/1/2 (first category, second poll)
    url(r'^(?P<category_id>\d+)/(?P<poll_id>\d+)/$',
        views.poll, name='question'),

    url(r'^get_chart/(?P<poll_id>\d+)/$',
        views.get_poll_chart, name='get_chart'),
    
    url(r'^get_timeline/(?P<poll_id>\d+)/$',
        views.get_poll_timeline, name='get_timeline'),

    # ex: localhost:8000/categories/
    url(r'^categories/$', views.get_all_categories, name='get_all_categories'),

    # ex: localhost:8000/about/
    url(r'^about/$', views.about, name='about'),

    # ex: localhost:8000/contact/
    url(r'^contact/', views.contact_us, name='contact_us'),

    # ex: localhost:8000/freeze_voting/(category_id)/(poll_id)
    url(r'^freeze_voting/(?P<poll_id>\d+)/$',
        views.freeze_voting, name='freeze_voting'),

    # ex: localhost:8000/delete_poll/(category_id)/poll_id/
    url(r'^delete_poll/(?P<poll_id>\d+)/$',
        views.delete_poll, name='delete_poll'),

    url(r'^vote/$',
        views.vote, name='vote'),
                       
    url(r'^change_vote/$',
        views.change_vote, name='change_vote'),
                       
    url(r'^delete_vote/$',
        views.delete_vote, name='delete_vote'),

    url(r'^new_comment/$',
        views.writecomment, name='writecomment'),

    url(r'^delete_comment/(?P<category_id>\d+)/(?P<poll_id>\d+)/(?P<comment_id>\d+)$',
        views.delete_comment, name='deletecomment'),
                       
    url(r'^like_comment/(?P<category_id>\d+)/(?P<poll_id>\d+)/(?P<comment_id>\d+)$',
        views.like_comment, name='likecomment'),
                       
    url(r'^unlike_comment/(?P<category_id>\d+)/(?P<poll_id>\d+)/(?P<comment_id>\d+)$',
        views.unlike_comment, name='unlikecomment'),
)
