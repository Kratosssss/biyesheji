# Generated by Django 2.1.7 on 2019-04-23 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs_app', '0018_auto_20190423_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='missionpackage',
            name='pic_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='图片数量'),
        ),
    ]
