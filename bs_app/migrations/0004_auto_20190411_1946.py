# Generated by Django 2.1.7 on 2019-04-11 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bs_app', '0003_auto_20190411_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pictures',
            old_name='ima_buget',
            new_name='img_budget',
        ),
    ]
