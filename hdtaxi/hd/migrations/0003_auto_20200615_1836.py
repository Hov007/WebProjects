# Generated by Django 3.0.6 on 2020-06-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd', '0002_car_sits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='sits',
        ),
        migrations.AddField(
            model_name='day',
            name='sits',
            field=models.IntegerField(default=7),
        ),
    ]