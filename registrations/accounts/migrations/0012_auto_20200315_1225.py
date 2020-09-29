# Generated by Django 3.0.3 on 2020-03-15 06:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200315_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='netbanking',
            name='Bank',
            field=models.CharField(default='Bank of Baroda', max_length=25),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2020, 3, 15, 6, 55, 27, 741025, tzinfo=utc), max_length=19),
        ),
    ]
