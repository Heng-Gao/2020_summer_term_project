# Generated by Django 2.1.4 on 2020-08-07 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0014_restaurant_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderId',
            fields=[
                ('first', models.IntegerField(primary_key=True, serialize=False)),
                ('id', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='realId',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]