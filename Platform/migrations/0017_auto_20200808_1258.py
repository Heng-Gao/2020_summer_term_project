# Generated by Django 3.0.5 on 2020-08-08 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0016_auto_20200807_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='image',
        ),
        migrations.AddField(
            model_name='tmprestaurant',
            name='image',
            field=models.ImageField(default=1, upload_to='image'),
        ),
    ]
