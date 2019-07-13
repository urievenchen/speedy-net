# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-13 13:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import speedy.core.base.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('last_visit', models.DateTimeField(auto_now_add=True, verbose_name='last visit')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='speedy_net_site_profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Speedy Net Profile',
                'verbose_name_plural': 'Speedy Net Profiles',
            },
            bases=(speedy.core.base.models.ValidateModelMixin, models.Model),
        ),
    ]
