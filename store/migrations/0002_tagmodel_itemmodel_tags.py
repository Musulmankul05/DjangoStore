# Generated by Django 5.0.6 on 2024-07-10 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=128)),
                ('slug', models.SlugField(max_length=128, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='itemmodel',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='store.tagmodel'),
        ),
    ]
