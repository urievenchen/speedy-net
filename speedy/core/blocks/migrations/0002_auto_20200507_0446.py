# Generated by Django 3.0.6 on 2020-05-07 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200121_1731'),
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='blocked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocking_entities', to='accounts.Entity', verbose_name='blocked user'),
        ),
        migrations.AlterField(
            model_name='block',
            name='blocker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_entities', to='accounts.Entity', verbose_name='user'),
        ),
    ]