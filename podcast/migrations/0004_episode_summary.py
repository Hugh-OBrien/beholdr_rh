# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-19 11:40
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0003_episode_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='summary',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]