# Generated by Django 2.2.7 on 2019-12-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('classID', models.CharField(max_length=40)),
                ('sessionID', models.IntegerField()),
                ('userID', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('superUserID', models.IntegerField()),
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('hwID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('classID', models.CharField(max_length=40)),
                ('userID', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=50)),
                ('classID', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=100)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('ID', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=40)),
                ('lastName', models.CharField(max_length=50)),
                ('studentID', models.IntegerField()),
            ],
        ),
    ]

