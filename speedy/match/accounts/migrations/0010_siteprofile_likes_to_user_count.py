# Generated by Django 3.1.6 on 2021-02-21 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match_accounts', '0009_siteprofile_profile_picture_months_offset'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='likes_to_user_count',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
    ]
