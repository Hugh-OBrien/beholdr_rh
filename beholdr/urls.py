from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from beholdr.views import homepage
from search import views as search_views
from podcast import views as podcast_views
from podcast.models import CastRoot
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

urlpatterns = [
    url(r'^$', homepage),
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^vhs/$',  podcast_views.vhs, name='vhs'),
    url(r'^pie/$',  podcast_views.pie, name='pie'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^tools/simplecast/', include('simple_cast.urls',\
                                       namespace="simple_cast")),
    url(r'^tools/iTunesReviews/', include('iTunesReviews.urls', \
                                    namespace ="iTunesReviews")),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
