# Generated by Django 2.1.7 on 2019-04-22 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs_app', '0015_auto_20190422_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pictures',
            name='img_budget',
            field=models.FloatField(blank=True, default=0.01, null=True),
        ),
    ]
