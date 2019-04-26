from biyesheji2.settings import MEDIA_ROOT
from bs_app.utils import FileUtils
import shutil
from bs_app import models
import cv2
from keras.models import load_model
import os

print('load model...')
model = load_model('D:\\pycharm\\biyesheji2\\templates\\keras_cifar10_trained_model.h5')  # 选取自己的.h模型名称
print('load done.')

#一定要添加这段代码，先测试一下，可以避免ValueError: Tensor Tensor("Placeholder:0", shape=(3, 3, 1, 32), dtype=float32)
#is not an element of this graph.的错误
print("test model...")
predict_img = cv2.imread('D:\\pycharm\\biyesheji2\\templates\\lqpic.jpg')
predict_img = cv2.resize(predict_img, (32, 32), 3)
predict_img = predict_img.reshape(1, 32, 32, 3).astype('float')
predict_img /= 255
predict = model.predict_classes(predict_img)
print("test done")


# 更新任务包信息 给定任务包图片数目和总价
def missionUpdate(request,mission_id, number):
    mission = models.MissionPackage.objects.get(id=mission_id)
    mission.pic_num = number
    mission.total_budget = mission.pic_num * float(mission.budget)
    mission.save()


# 把任务包存入数据库 把单价 和 描述 存入
def missionToDatabse(request, mp):
    client_id = request.session['client_id']
    client = models.ClientInfo.objects.get(id=client_id)

    # 给默认值
    budget = float(request.POST.get('budget', None)) if request.POST.get('budget', None) else 0.01
    description = request.POST.get('description', None) if request.POST.get('description', None) else ""
    if mp:
        # 存入任务包信息
        mission = models.MissionPackage()
        mission.client_id = client
        mission.mission = mp
        mission.budget = budget
        mission.description = description
        mission.save()
    return mission.id


# 将上传的图片包中的数据移至资源文件并保存在数据库 同时给这些图片打上一个系统标签
def uploadfile_to_database(imglist, path, mission_pickage_name, mission_id):
    mission = models.MissionPackage.objects.get(id=mission_id)
    # 存入图片数据库
    for img_name in imglist:
        oldname = path + mission_pickage_name + '/' + img_name
        newname = MEDIA_ROOT + '/picture_imgs/' + img_name
        # 检查重名
        newname = FileUtils.check_filename_available(newname)
        # 复制文件
        shutil.copyfile(oldname, newname)
        # 得到最后的文件名
        img_name_new = FileUtils.get_last_filename(newname)
        img = models.Pictures()
        img.mission = mission
        img.img_budget = mission.budget
        img.img_address = 'picture_imgs/' + img_name_new
        img.save()

    # 对图片报中的每一张图片给一个系统标签
    tobe_predicit_list = models.Pictures.objects.filter(mission=mission)
    # 载入模型 放到init里了
    predict_catagory = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship',
                        'truck']
    print(predict_catagory)
    img_dir = 'D:\\pycharm\\biyesheji2\\static\\media\\'
    for tobe_predicit_img in tobe_predicit_list:
        # 依次读入图片并预测
        # 使用模型，在得到用户输入时会调用以下两个函数进行实时文本分类

        predict_img = cv2.imread(img_dir + str(tobe_predicit_img.img_address))
        predict_img = cv2.resize(predict_img, (32, 32), 3)
        predict_img = predict_img.reshape(1, 32, 32, 3).astype('float')
        predict_img /= 255
        global model
        predict = model.predict_classes(predict_img)
        predict = int(predict)
        predict = int(predict)
        # print(predict_catagory[predict])
        models.Pictures.objects.filter(img_address=tobe_predicit_img.img_address).update(
            predict_tag=predict_catagory[predict])

