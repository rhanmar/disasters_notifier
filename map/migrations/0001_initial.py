# Generated by Django 3.2.8 on 2021-11-22 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('coordinates', models.CharField(max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('verified', models.BooleanField(default=False)),
                ('disaster_type', models.CharField(choices=[('fire', 'fire'), ('water', 'water'), ('geo', 'geo'), ('meteo', 'meteo')], default='fire', max_length=80)),
                ('disaster_level', models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, max_length=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_points', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
