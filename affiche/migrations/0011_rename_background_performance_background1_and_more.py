# Generated by Django 4.2.13 on 2024-05-23 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiche', '0010_alter_performance_subtitle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='background',
            new_name='background1',
        ),
        migrations.AddField(
            model_name='performance',
            name='background2',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='background3',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
    ]
