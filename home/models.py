from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)
    #pages = Page.objects.all()[0].url
    #print dir(pages[0].get_descendants())
    
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
