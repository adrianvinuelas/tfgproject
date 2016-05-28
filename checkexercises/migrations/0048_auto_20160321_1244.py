# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-21 12:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('checkexercises', '0047_auto_20160318_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentexercise',
            name='data',
            field=models.CharField(default=datetime.datetime(2016, 3, 21, 12, 44, 44, 635409, tzinfo=utc), max_length=10000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentexercise',
            name='rankingerrors',
            field=models.TextField(default=datetime.datetime(2016, 3, 21, 12, 44, 53, 11734, tzinfo=utc)),
            preserve_default=False,
        ),
    ]