# Generated by Django 3.0.5 on 2020-07-19 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
