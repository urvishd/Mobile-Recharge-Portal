# Generated by Django 3.0.3 on 2020-03-15 11:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20200315_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2020, 3, 15, 11, 24, 15, 7498, tzinfo=utc), max_length=19),
        ),
    ]
