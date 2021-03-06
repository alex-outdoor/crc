# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 23:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Created date', null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='Updated date', null=True)),
                ('company_name', models.CharField(blank=True, help_text='Name of the company', max_length=100, null=True)),
                ('contact_name', models.CharField(blank=True, help_text='Name of the contact', max_length=100, null=True)),
                ('contact_email', models.EmailField(blank=True, help_text='Email of the contact', max_length=254, null=True, verbose_name='email address')),
                ('address', models.CharField(blank=True, help_text='Address', max_length=200, null=True)),
                ('postal_code', models.CharField(blank=True, help_text='Postal Code', max_length=20, null=True)),
                ('city', models.CharField(blank=True, help_text='City', max_length=50, null=True)),
                ('province', models.CharField(blank=True, help_text='Province', max_length=50, null=True)),
                ('country', models.CharField(blank=True, help_text='Country', max_length=30, null=True)),
                ('main_phone', models.CharField(blank=True, help_text='Main phone number', max_length=30, null=True)),
                ('direct_number', models.CharField(blank=True, help_text='Direct number', max_length=30, null=True)),
                ('fax', models.CharField(blank=True, help_text='Fax number', max_length=30, null=True)),
                ('notes', models.CharField(blank=True, help_text='Notes', max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
