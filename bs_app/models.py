from django.db import models
from django.utils.html import format_html

import os
from biyesheji2.settings import MEDIA_ROOT
from django.core.files import File

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
# 本数据表修改放这里

class ClientInfo(models.Model):

    id = models.AutoField(primary_key=True)
    client_name = models.CharField(verbose_name='客户名', max_length=16,null=False)
    password = models.CharField(max_length=16,null=False)
    email = models.EmailField(verbose_name='email',null=False)
    client_img = models.ImageField(null=True, blank=True, upload_to="client_imgs")
    wallet = models.FloatField(verbose_name='钱包', default=100)

    def __str__(self):
        return self.client_name


class UserInfo(models.Model):

    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=16, null=False)
    password = models.CharField(max_length=16, null=False)
    email = models.EmailField(null=True, blank=True)
    user_img = models.ImageField(null=True, blank=True, upload_to="user_imgs")
    wallet = models.FloatField(verbose_name='钱包', default=0)

    def user_img_show(self):
        if self.user_img:
            return format_html(
                '<img src="{}" width="50px"/>',
                self.user_img.url,
            )
        else:
            pass

    user_img_show.short_description = u'照片'


class Pictures(models.Model):

    id = models.AutoField(primary_key=True)
    # cascade 删除图片包时删除对应图片
    mission = models.ForeignKey('MissionPackage', blank=True, default='', on_delete=models.CASCADE)
    predict_tag = models.CharField(verbose_name='系统标签', null=True, blank=True, max_length=20)
    final_tag = models.CharField(verbose_name='最终标签', null=True, blank=True, max_length=20)
    img_tag_num = models.IntegerField(verbose_name='标记次数', default=0)
    img_address = models.ImageField(verbose_name='图片地址', null=False, upload_to="picture_imgs")
    img_budget = models.FloatField(verbose_name='单价', null=True, blank=True, default=0.01)



    def img_show(self):
        if self.img_address:
            return format_html(
                '<img src="{}" width="50px"/>',
                self.img_address.url,
            )
        else:
            pass

    img_show.short_description = u'照片'


class Matchup(models.Model):
    id = models.AutoField(primary_key=True)
    matchup_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    matchup_picture = models.ForeignKey('Pictures', on_delete=models.CASCADE)
    matchup_tag = models.ForeignKey('Tag', on_delete=models.CASCADE)





class Tag(models.Model):

    id = models.AutoField(primary_key=True)
    tag_description = models.TextField(verbose_name="标签")

    def __str__(self):
        return self.tag_description


class MissionPackage(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey('ClientInfo', blank=True, default='', on_delete=models.DO_NOTHING)
    pic_num = models.IntegerField(verbose_name="图片数量", blank=True,null=True)
    mission = models.FileField(verbose_name='任务包', null=False, upload_to='missionpackages')
    budget = models.FloatField(verbose_name='单价', null=True, blank=True, default=10)
    total_budget = models.FloatField(verbose_name='总价', null=True, blank=True)
    begintime = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    description = models.CharField(verbose_name='介绍', max_length=100, null=True, blank=True)
    isfinished = models.BooleanField(verbose_name='是否完成', default=False)

