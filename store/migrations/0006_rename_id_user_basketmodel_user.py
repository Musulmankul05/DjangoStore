# Generated by Django 5.0.6 on 2024-08-22 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_basketmodel_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basketmodel',
            old_name='id_user',
            new_name='user',
        ),
    ]
