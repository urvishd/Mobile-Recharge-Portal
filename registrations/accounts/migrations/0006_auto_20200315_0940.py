# Generated by Django 3.0.3 on 2020-03-15 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200315_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
