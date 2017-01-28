from django.shortcuts import render
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.wagtailsearch.backends import get_search_backend

from models import Episode, CastRoot

from django.db import models
from wagtail.wagtailcore.models import Page, Orderable


def home(request, cast = ""):
    page = request.GET.get('page', 1)

    #get the cast id from the request or send back home
    if cast == "":
        return redirect('../')

    #Search for everything published with the cast name
    eps = Episode.objects.filter(podcast=cast).order_by('published_date').reverse()

    #paginate and render
    paginator = Paginator(eps, 9)

    #get CastRoot object
    root = CastRoot.objects.get(pod_id=int(cast))
    
    for a in CastRoot.objects.all():
        print (a.pod_id)

    try:
        eps = paginator.page(page)
    except PageNotAnInteger:
        eps = paginator.page(1)
    except EmptyPage:
        eps = paginator.page(paginator.num_pages)
        
    return render(request, 'podcast/home.html', {
        'eps':eps,
        'root':root,
        'pagination_loop' :range( int(page),  ),
    })

def vhs(request):
    """
    Add a custom view function for each podcast and generate the homepage
    """
    return home(request, cast="1105")

def pie(request):
    return home(request, cast="2120")
