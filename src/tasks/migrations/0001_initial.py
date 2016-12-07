# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 15:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owning_organisation', models.CharField(max_length=128)),
                ('required_permission_name', models.CharField(blank=True, default='', max_length=128)),
                ('description', models.CharField(max_length=64)),
                ('category', models.CharField(choices=[('update', 'Update datasets'), ('fix', 'Fix datasets'), ('improve', 'Improve datasets'), ('accounts', 'Manage accounts')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserHiddenTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]