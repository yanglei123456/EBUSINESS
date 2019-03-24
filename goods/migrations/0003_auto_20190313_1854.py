# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20190313_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='picture',
            field=models.FileField(verbose_name='/upload/', upload_to=''),
        ),
    ]
