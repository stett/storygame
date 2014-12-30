# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_story_complete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='complete',
            new_name='completed',
        ),
        migrations.AddField(
            model_name='story',
            name='size',
            field=models.PositiveIntegerField(default=5, max_length=5),
            preserve_default=True,
        ),
    ]
