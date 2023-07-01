# Generated by Django 4.2.1 on 2023-07-01 12:01

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_max_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='booking_end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 8, 12, 1, 17, 606477, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='event',
            name='booking_start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]