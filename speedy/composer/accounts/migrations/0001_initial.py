# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 15:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20170117_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='+', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('last_visit', models.DateTimeField(auto_now_add=True, verbose_name='last visit')),
                ('is_active', models.BooleanField(default=False, verbose_name='indicates if a user has ever logged in to the site')),
            ],
            options={
                'verbose_name': 'Speedy Composer Profile',
                'verbose_name_plural': 'Speedy Composer Profiles',
            },
        ),
    ]
