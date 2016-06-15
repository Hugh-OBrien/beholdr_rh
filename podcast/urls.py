from django.conf.urls import url

from podcast.views import home

urlpatterns = [
    url(r'^$', vhs, name='vhs'),
    url(r'', include(wagtail_urls)),
]
