# Generated by Django 3.2.10 on 2022-04-07 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopIn', '0004_orders_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='img',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
