# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_auto_20141130_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='complete',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
