# Generated by Django 3.2.9 on 2021-11-23 10:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20211121_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentbook',
            name='returnDate',
            field=models.DateField(default=datetime.date.today),
        ),
    ]