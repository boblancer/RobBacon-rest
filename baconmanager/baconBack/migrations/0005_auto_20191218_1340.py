# Generated by Django 2.2.7 on 2019-12-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baconBack', '0004_auto_20191218_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='userID',
            field=models.CharField(max_length=40),
        ),
    ]
