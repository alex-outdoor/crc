# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 01:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crccloud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='Creator', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
