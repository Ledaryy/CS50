# Generated by Django 3.0.8 on 2020-08-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_bids_currentbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
