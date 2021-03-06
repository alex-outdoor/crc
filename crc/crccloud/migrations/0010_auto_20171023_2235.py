# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crccloud', '0009_auto_20171021_0210'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='contact_email',
            field=models.EmailField(blank=True, help_text='Email of the contact if BID specific', max_length=254, null=True, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='bid',
            name='contact_name',
            field=models.CharField(blank=True, help_text='Name of the contact if BID specific', max_length=100, null=True),
        ),
    ]
