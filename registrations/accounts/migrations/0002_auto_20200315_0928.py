# Generated by Django 3.0.3 on 2020-03-15 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.DateTimeField(max_length=50),
        ),
    ]
