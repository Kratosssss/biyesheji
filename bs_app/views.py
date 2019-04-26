from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from biyesheji2.settings import MEDIA_ROOT
import os
from bs_app import models
from bs_app.utils import FileUtils,UploadUtils,LoginUtils
from django.db.models import Avg, Min, Max, Count, Sum
import random


# Create your views here.


def index(request):
    return redirect('/loginUser',)


# 主页
def mainpage(request): # request是必须带的实例。类似class下方法必须带self一样
    return render(request, "mainpage.html",)


# 用户登陆
def loginUser(request):
    # 如果已经登陆直接去主界面
    if request.session.get('is_login', None):
        return redirect('/mainpage', )

    # 直接输入网址
    if request.method == "GET":
        return render(request, "loginUser.html", )

    # 通过表单提交
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        try:
            if LoginUtils.UserLogin(request,username,password):
                return redirect('/mainpage', )
        except:
            messages.add_message(request, messages.WARNING, '账号密码错误')
        return render(request, 'loginUser.html', )

# 客户登陆
def loginClient(request):
    # 如果已经登陆直接去主界面
    if request.session.get('is_login', None):
        return redirect('/mainpage', )

    # 通过网址登陆
    if request.method == "GET":
        return render(request, "loginClient.html", )

    # 表单提交
    if request.method == "POST":
        clientname = request.POST.get('clientname', None)
        password = request.POST.get('clientpassword', None)
        try:
            if LoginUtils.ClientLogin(request,clientname,password):
                return redirect('/mainpage',)
        except:
            messages.add_message(request, messages.WARNING, '账号密码错误')
        return render(request, "loginClient.html", )


# 登出
def logout(request):
    if not request.session.get('is_login', None):
    # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def missionUpload(request):
    return render(request, 'missionUpload.html')


# 上传需要标注的任务包 客户独有
def upload(request):
    if request.method == "POST":
        mp = request.FILES.get("missionPackage", None)
        path = MEDIA_ROOT + '/picture_imgs/'
        # 任务包存入数据库
        mission_id = UploadUtils.missionToDatabse(request, mp)
        # 解压文件包 m文件包名称 不含后缀
        mission_pickage_name = FileUtils.unzip(path, mp).group()
        # 得到任务包中的每一张图片名字
        imglist = os.listdir(path + mission_pickage_name)
        # 更新任务包信息 把图片数目 和价格给上
        UploadUtils.missionUpdate(request, mission_id, len(imglist))
        # 复制图片文件入资源文件夹 并填入数据库
        UploadUtils.uploadfile_to_database(imglist, path, mission_pickage_name, mission_id)
        return render(request, 'missionUpload.html', )


# 客户查看任务
def missionShow(request):
    # 得到客户数据
    client_id = request.session['client_id']
    client = models.ClientInfo.objects.get(id=client_id)
    mission = models.MissionPackage.objects.filter(client_id=client)

    return render(request, 'missionShow.html', {"missions": mission})


# 用户挑选任务
def missionChose(request):
    mission = models.MissionPackage.objects.filter(isfinished=False)
    return render(request, 'missionChose.html', {"missions": mission})


# 用户打标签页面 显示第一张
def imageShow(request):
    # 得到用户model
    user_id = request.session['user_id']
    user = models.UserInfo.objects.get(id=user_id)
    # mission_id 使用cookie传递
    mission_id = request.COOKIES.get('mission_id')
    # 得到当前任务包信息
    mission = models.MissionPackage.objects.get(id=mission_id)
    # 得到标记次数小于5并且属于该任务包的图片集合
    imgs = models.Pictures.objects.filter(mission_id=mission, img_tag_num__lt=5)

    # 用来判断图片是否被用户标记 默认已标记
    # 遍历小于5次的图片 取出第一个没有被该用户 标签的图像
    pd = True
    for img in imgs:
        pd = True
        matchs = models.Matchup.objects.filter(matchup_picture=img)
        # 此用户已经标记此张图片
        for match in matchs:
            if match.matchup_user.id == user.id:
                pd = False
                # print("这张图片已被标记")
                break
        if pd is False:
            # print("检验下一张图片")
            continue
        elif pd is True:
            # print("决定就是这张图片了")
            break
    if pd is True:
        # print("决定就是这张图片了")
        # mode1 系统预测
        return render(request, "imageShow.html", {'img': img})

        # mode2  系统随机返回一个标签
        # random_tag = models.Tag.objects.all()[random.randint(0, 9)]
        # return render(request, 'imageShow.html', {'img': img, 'random_tag': random_tag})

        # mode3 系统返回其他人对这张图片的标签
        # others_matchs = models.Matchup.objects.filter(matchup_picture=img)
        # print(type(others_matchs))
        # return render(request, 'imageShow.html', {'img': img, 'others_matchs': others_matchs})

        # mode4 返回最高选项的标签
        # max_match = models.Matchup.objects.filter(matchup_picture=img).values('matchup_tag').annotate(tag_count=Count('matchup_tag')).order_by('-tag_count')[0]
        # # SELECT matchup_tag_id, COUNT(matchup_tag_id) AS tag_count
        # # WHERE matchup_picture_id = 1168
        # # GROUP BY matchup_tag_id
        # # ORDER BY tag_count DESC
        # # print(max_match.query)
        # print(max_match)
        # max_tag = models.Tag.objects.get(id=max_match['matchup_tag'])
        # print(max_tag.tag_description)
        # return render(request, 'imageShow.html', {'img': img, 'max_tag': max_tag})

    else:
        # print("都标记完了")
        return render(request, "imageShow.html", )


# 将用户选择的标签存入数据库
def tagChose(request):
    # 从session中的到用户信息 和 mission信息
    user_id = request.session['user_id']
    user = models.UserInfo.objects.get(id=user_id)

    # 得到传过来的图片信息和标签信息
    img_address = request.POST.get('img', None)
    tag_des = request.POST.get('tag', None)

    # 搜索到数据库中图片信息 和tag信息
    img = models.Pictures.objects.get(img_address=img_address)
    tag = models.Tag.objects.get(tag_description=tag_des)

    # 图片标记次数+1 5次上线
    img.img_tag_num += 1
    img.save()
    user.wallet += img.img_budget
    user.save()
    request.session['wallet'] = user.wallet

    models.Matchup.objects.create(matchup_user=user, matchup_picture=img, matchup_tag=tag)
    return redirect("/imageShow/")
