from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey

import json
import requests

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True

                       
class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True

class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('Episode', related_name='related_links')

class Episode(Page):
    podcast = models.CharField(max_length=10, default="")
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    epID = models.CharField(max_length=10, default=0)
    description = RichTextField(blank=True)
    summary = RichTextField(blank=True)
    published_date = models.CharField(max_length=50, default="")
    image_URL= models.CharField(max_length=300, default="")
    quote= models.CharField(max_length=300, default="", blank=True)
    #others = (Page.objects.all()[3].get_children()[1])

    content_panels = Page.content_panels + [
        FieldPanel('podcast'),
        FieldPanel('epID'),
        FieldPanel('summary'),
        FieldPanel('description'),
        FieldPanel('quote'),
        ImageChooserPanel('main_image'),
        FieldPanel('published_date'),
        InlinePanel('related_links', label="Related links")
    ]

    search_fields = Page.search_fields + [ # Inherit search_fields from Page
        index.FilterField('podcast'),
    ]

class CastRoot(Page):
    description = RichTextField(blank=True)
    #pod id used for auto update of episodes
    pod_id = models.IntegerField(default=1)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        FieldPanel('pod_id'),
        ImageChooserPanel('main_image')
    ]


    

