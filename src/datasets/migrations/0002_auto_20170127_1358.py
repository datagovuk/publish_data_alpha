# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-27 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='location',
        ),
        migrations.AddField(
            model_name='dataset',
            name='locations',
            field=models.ManyToManyField(related_name='datasets', to='datasets.Location'),
        ),
    ]