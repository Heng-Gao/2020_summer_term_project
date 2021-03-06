# Generated by Django 2.1.4 on 2020-08-06 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0010_auto_20200725_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tmp',
            fields=[
                ('t_id', models.AutoField(primary_key=True, serialize=False)),
                ('t_name', models.CharField(max_length=15)),
                ('t_addr', models.CharField(max_length=2)),
                ('t_tel', models.CharField(max_length=15)),
                ('t_email', models.EmailField(max_length=254)),
                ('t_status', models.IntegerField(default=1)),
            ],
        ),
    ]
