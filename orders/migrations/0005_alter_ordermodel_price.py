# Generated by Django 5.0.6 on 2024-08-19 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_delivered_ordermodel_is_delivered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=36),
        ),
    ]
