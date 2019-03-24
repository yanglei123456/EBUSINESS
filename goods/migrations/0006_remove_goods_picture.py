# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20190313_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='picture',
        ),
    ]
