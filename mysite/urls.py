from django.conf.urls import patterns, include, url, static
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mysite import settings

urlpatterns = patterns('',
    url(r'^', include('polls.urls')),
    url(r'^', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

