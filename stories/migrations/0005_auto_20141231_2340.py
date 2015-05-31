# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_auto_20141130_2219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storyauthor',
            options={},
        ),
        migrations.RemoveField(
            model_name='storyauthor',
            name='order',
        ),
        migrations.AddField(
            model_name='storyauthor',
            name='next',
            field=models.OneToOneField(related_name='previous', null=True, blank=True, to='stories.StoryAuthor'),
            preserve_default=True,
        ),
    ]
