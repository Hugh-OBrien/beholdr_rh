from django import template
from podcast.models import CastRoot

register = template.Library()

@register.simple_tag
def all_podcasts():
    return CastRoot.objects.all()

#register.filter('podcasts', all_podcasts)
