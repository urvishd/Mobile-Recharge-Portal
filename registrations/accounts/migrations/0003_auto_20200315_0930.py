# Generated by Django 3.0.3 on 2020-03-15 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200315_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.DateTimeField(blank=True, max_length=50),
        ),
    ]