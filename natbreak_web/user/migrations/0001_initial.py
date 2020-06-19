# Generated by Django 3.0.7 on 2020-06-09 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('login_name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('nickname', models.CharField(max_length=20)),
                ('password', models.CharField(default='123456', max_length=32)),
                ('head_portrait', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=16)),
                ('register_time', models.DateTimeField()),
                ('network_traffic', models.BigIntegerField()),
                ('used_traffic', models.BigIntegerField()),
            ],
        ),
    ]