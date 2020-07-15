# Generated by Django 2.1.4 on 2020-03-15 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwc', '0003_auto_20200313_2319'),
    ]

    operations = [
        migrations.CreateModel(
            name='courseinfo',
            fields=[
                ('course_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('course_number', models.CharField(max_length=4)),
                ('course_name', models.CharField(max_length=15)),
                ('course_credit', models.CharField(max_length=2)),
                ('course_status', models.CharField(max_length=8)),
                ('teacher_number', models.CharField(max_length=8)),
                ('teacher_name', models.CharField(max_length=8)),
                ('student_number', models.CharField(max_length=8)),
                ('student_name', models.CharField(max_length=8)),
                ('student_score', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='term',
            fields=[
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=8)),
            ],
        ),
    ]
