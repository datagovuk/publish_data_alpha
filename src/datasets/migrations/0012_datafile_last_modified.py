# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0011_organisation_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='last_modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
