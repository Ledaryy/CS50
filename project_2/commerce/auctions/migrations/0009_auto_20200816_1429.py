# Generated by Django 3.0.8 on 2020-08-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctions_currentbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='description',
            field=models.CharField(max_length=256),
        ),
    ]