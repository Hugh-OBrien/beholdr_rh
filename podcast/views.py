from django.shortcuts import render
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.wagtailsearch.backends import get_search_backend

from models import Episode, CastRoot

from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from dateutil import parser

def home(request, cast = ""):
    page = request.GET.get('page', 1)

    #get the cast id from the request or send back home
    if cast == "":
        return redirect('../')

    #Search for everything published with the cast name
    eps = Episode.objects.filter(podcast=cast).order_by('published_date').reverse()

    for e in eps:
        e.published_date = parser.parse(e.published_date).date
    #paginate and render
    paginator = Paginator(eps, 9)

    #get CastRoot object
    root = CastRoot.objects.get(pod_id=int(cast))

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

def search(request):
    page = request.GET.get('page', 1)
    try:
        search_term = request.POST['search_term']
    except:
        search_term = ""

    if search_term == "":
        eps = []
    else:
        eps = Episode.objects.all().search(search_term)

    for e in eps:
        e.published_date = parser.parse(e.published_date).date
    paginator = Paginator(eps, 9)    
    try:
        eps = paginator.page(page)
    except PageNotAnInteger:
        eps = paginator.page(1)
    except EmptyPage:
        eps = paginator.page(paginator.num_pages)

    return render(request, 'podcast/search.html', {
        'eps':eps,
        'search':search_term
    })

def vhs(request):
    """
    Add a custom view function for each podcast and generate the homepage
    """
    return home(request, cast="1105")

def pie(request):
    return home(request, cast="2120")
