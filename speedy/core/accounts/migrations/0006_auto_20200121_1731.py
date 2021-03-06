# Generated by Django 2.1.15 on 2020-01-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200106_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='notify_on_message',
            field=models.SmallIntegerField(choices=[(1, 'Notify me'), (0, "Don't notify me")], default=1, verbose_name='On new messages'),
        ),
    ]
