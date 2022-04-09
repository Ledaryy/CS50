# Generated by Django 3.0.8 on 2020-08-15 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200815_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('watchlist', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='watchlist',
        ),
    ]