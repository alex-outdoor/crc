# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 02:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crccloud', '0008_auto_20171020_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverable',
            name='bid',
            field=models.ForeignKey(help_text='Deliverables linked to this BID', on_delete=django.db.models.deletion.CASCADE, related_name='deliverables', to='crccloud.Bid'),
        ),
        migrations.AlterField(
            model_name='methodology',
            name='respondent',
            field=models.ForeignKey(help_text='Methodology linked to this respondent group', on_delete=django.db.models.deletion.CASCADE, related_name='methodologies', to='crccloud.Respondent'),
        ),
        migrations.AlterField(
            model_name='respondent',
            name='bid',
            field=models.ForeignKey(help_text='Respondent group attached to this BID', on_delete=django.db.models.deletion.CASCADE, related_name='respondents', to='crccloud.Bid'),
        ),
    ]
