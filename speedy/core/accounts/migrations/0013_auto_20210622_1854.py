# Generated by Django 3.1.12 on 2021-06-22 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20201010_0757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useremailaddress',
            options={'ordering': ('date_created',), 'verbose_name': 'email address', 'verbose_name_plural': 'email addresses'},
        ),
    ]
