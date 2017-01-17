# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 15:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20170117_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cause',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.Entity')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.entity',),
        ),
    ]
