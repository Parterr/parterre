# Generated by Django 4.2.13 on 2024-06-03 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiche', '0033_performancefiles_performance_image_carousel'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancefiles',
            name='for_performance',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='affiche.performance'),
            preserve_default=False,
        ),
    ]
