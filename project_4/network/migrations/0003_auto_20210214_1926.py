# Generated by Django 3.0.8 on 2021-02-14 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='post',
            name='img',
        ),
    ]