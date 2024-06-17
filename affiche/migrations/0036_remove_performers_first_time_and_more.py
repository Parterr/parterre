# Generated by Django 4.2.13 on 2024-06-14 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiche', '0035_row_seat_alter_performancefiles_options_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performers',
            name='first_time',
        ),
        migrations.RemoveField(
            model_name='performers',
            name='performance',
        ),
        migrations.RemoveField(
            model_name='performers',
            name='role',
        ),
        migrations.CreateModel(
            name='PerformancePerformers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='affiche.performance')),
                ('performer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='affiche.performers')),
            ],
        ),
    ]
