# Generated by Django 3.2.10 on 2022-04-07 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopIn', '0006_auto_20220407_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='products',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='productCategory',
            field=models.CharField(max_length=50),
        ),
    ]
