# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-13 13:46
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import speedy.core.accounts.models
import speedy.core.base.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', speedy.core.base.models.SmallUDIDField(db_index=True, max_length=15, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator(message='id contains illegal characters.', regex='^[1-9][0-9]{14}$')], verbose_name='ID')),
                ('username', models.CharField(error_messages={'unique': 'This username is already taken.'}, max_length=255, unique=True, verbose_name='username')),
                ('slug', models.CharField(error_messages={'unique': 'This username is already taken.'}, max_length=255, unique=True, verbose_name='username (slug)')),
            ],
            options={
                'verbose_name': 'entity',
                'verbose_name_plural': 'entities',
                'ordering': ('id',),
            },
            bases=(speedy.core.accounts.models.CleanAndValidateAllFieldsMixin, speedy.core.base.models.ValidateModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UserEmailAddress',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', speedy.core.base.models.RegularUDIDField(db_index=True, max_length=20, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator(message='id contains illegal characters.', regex='^[1-9][0-9]{19}$')], verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='is confirmed')),
                ('is_primary', models.BooleanField(default=False, verbose_name='is primary')),
                ('confirmation_token', models.CharField(blank=True, max_length=32, verbose_name='confirmation token')),
                ('confirmation_sent', models.IntegerField(default=0, verbose_name='confirmation sent')),
                ('access', speedy.core.accounts.models.UserAccessField(choices=[(1, 'Only me'), (2, 'Me and my friends'), (4, 'Anyone')], default=1, verbose_name='who can see this email')),
            ],
            options={
                'verbose_name': 'email address',
                'verbose_name_plural': 'email addresses',
                'ordering': ('date_created', 'id'),
            },
            bases=(speedy.core.accounts.models.CleanAndValidateAllFieldsMixin, speedy.core.base.models.ValidateModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.Entity')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name_en', models.CharField(max_length=75, verbose_name='first name')),
                ('first_name_he', models.CharField(max_length=75, verbose_name='first name')),
                ('last_name_en', models.CharField(max_length=75, verbose_name='last name')),
                ('last_name_he', models.CharField(max_length=75, verbose_name='last name')),
                ('gender', models.SmallIntegerField(choices=[(1, 'Female'), (2, 'Male'), (3, 'Other')], verbose_name='I am')),
                ('date_of_birth', models.DateField(verbose_name='date of birth')),
                ('diet', models.SmallIntegerField(choices=[(0, 'Unknown'), (1, 'Vegan (eats only plants and fungi)'), (2, "Vegetarian (doesn't eat fish and meat)"), (3, 'Carnist (eats animals)')], default=0, verbose_name='diet')),
                ('smoking_status', models.SmallIntegerField(choices=[(0, 'Unknown'), (1, 'No'), (2, 'Sometimes'), (3, 'Yes')], default=0, verbose_name='smoking status')),
                ('marital_status', models.SmallIntegerField(choices=[(0, 'Unknown'), (1, 'Single'), (2, 'Divorced'), (3, 'Widowed'), (4, 'In a relationship'), (5, 'In an open relationship'), (6, "It's complicated"), (7, 'Separated'), (8, 'Married')], default=0, verbose_name='marital status')),
                ('city_en', models.CharField(blank=True, max_length=120, null=True, verbose_name='city or locality')),
                ('city_he', models.CharField(blank=True, max_length=120, null=True, verbose_name='city or locality')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('access_dob_day_month', speedy.core.accounts.models.UserAccessField(choices=[(1, 'Only me'), (2, 'Me and my friends'), (4, 'Anyone')], default=1, verbose_name='who can view my birth month and day')),
                ('access_dob_year', speedy.core.accounts.models.UserAccessField(choices=[(1, 'Only me'), (2, 'Me and my friends'), (4, 'Anyone')], default=1, verbose_name='who can view my birth year')),
                ('notify_on_message', models.PositiveIntegerField(choices=[(1, 'Notify me'), (0, "Don't notify me")], default=1, verbose_name='on new messages')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('-last_login', 'id'),
                'swappable': 'AUTH_USER_MODEL',
            },
            bases=('accounts.entity', models.Model),
        ),
        migrations.AddField(
            model_name='useremailaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_addresses', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]