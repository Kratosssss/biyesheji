# Generated by Django 2.1.7 on 2019-04-21 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs_app', '0011_pictures_predict_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='pictures',
            name='img_tag_num',
            field=models.IntegerField(default=0),
        ),
    ]
