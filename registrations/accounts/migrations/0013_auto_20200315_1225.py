# Generated by Django 3.0.3 on 2020-03-15 06:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20200315_1225'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NetBanking',
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2020, 3, 15, 6, 55, 49, 358728, tzinfo=utc), max_length=19),
        ),
    ]
