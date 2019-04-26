# Generated by Django 2.1.7 on 2019-04-21 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs_app', '0012_pictures_img_tag_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pictures',
            name='img_tag',
        ),
        migrations.AlterField(
            model_name='pictures',
            name='img_budget',
            field=models.IntegerField(blank=True, default=0.01, null=True),
        ),
    ]