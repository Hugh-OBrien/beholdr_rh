from __future__ import absolute_import
from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Max
from podcast.models import Episode, CastRoot, Host, HomePage
from wagtail.wagtailsearch.backends import get_search_backend

def homepage(request):

    recent_casts = []
    shows_data = []

    casts = CastRoot.objects.all()
    for cast in casts:
        # get the most recent episode of each podcast with a quote
        try:
            sode = Episode.objects.filter(
                podcast=int(cast.pod_id)).exclude(quote='').latest('published_date')
            recent_casts.append(sode)
        except:
            print cast

        # also get all the podcasts with their most recent episode data
        cast_data = [cast, Episode.objects.filter(
            podcast=int(cast.pod_id)).latest('published_date')]
        shows_data.append(cast_data)

    template = loader.get_template('homepage.html')
    context = RequestContext(request, {'carousel': recent_casts,
                                       'shows': shows_data})
    return HttpResponse(template.render(context))

def contact(request):
    hosts = Host.objects.all()
    network = HomePage.objects.all()[0]
    for host in hosts:
        host.twitter_handle = "https://twitter.com/{0}/profile_image?size=original".format(host.twitter_handle)
    context = RequestContext(request, {'hosts': hosts,
                                       'network': network})
    template = loader.get_template('contact.html')
    return HttpResponse(template.render(context))
