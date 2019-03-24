# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_remove_goods_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='picture',
            field=models.FileField(default='i', upload_to='upload'),
        ),
    ]
