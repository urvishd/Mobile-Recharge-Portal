# Generated by Django 3.0.3 on 2020-03-15 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200315_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]