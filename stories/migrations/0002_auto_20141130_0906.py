# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storyauthor',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='storyauthor',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='storyauthor',
            name='story',
            field=models.ForeignKey(related_name='authors', to='stories.Story'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='storychunk',
            name='story',
            field=models.ForeignKey(related_name='chunks', to='stories.Story'),
            preserve_default=True,
        ),
    ]
