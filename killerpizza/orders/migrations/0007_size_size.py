# Generated by Django 3.0.6 on 2020-05-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200527_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='size',
            field=models.CharField(default='Size', max_length=64),
        ),
    ]