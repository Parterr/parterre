# Generated by Django 4.2.13 on 2024-06-02 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiche', '0023_performance_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='history',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
    ]
