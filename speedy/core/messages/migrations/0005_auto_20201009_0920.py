# Generated by Django 3.1.1 on 2020-10-09 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_messages', '0004_auto_20200607_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='messages', to='core_messages.chat', verbose_name='chat'),
        ),
    ]
