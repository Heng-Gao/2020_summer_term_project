# Generated by Django 2.1.4 on 2020-03-15 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwc', '0006_auto_20200315_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='opened_course',
            fields=[
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('credit', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=15)),
                ('teacher_name', models.CharField(max_length=8)),
            ],
        ),
    ]
