# Generated by Django 3.0.8 on 2020-08-16 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200815_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='currentBid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
