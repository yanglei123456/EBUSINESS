# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('address', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('picture', models.FileField(verbose_name='./upload', upload_to='')),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='goods.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField()),
                ('address', models.ForeignKey(to='goods.Address')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.ForeignKey(to='goods.Orders'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to='goods.User'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(to='goods.User'),
        ),
    ]
