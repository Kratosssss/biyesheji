import cv2
from keras.models import load_model
import os


model = load_model('keras_cifar10_trained_model.h5')  #选取自己的.h模型名称

# image = cv2.imread('xjpic.jpg')
# img = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY) # RGB图像转为gray
# # 需要用reshape定义出例子的个数，图片的 通道数，图片的长与宽。具体的参加keras文档
# img = (img.reshape(1, 3, 32, 32)).astype('float32') / 255


#要预测的图片类别
predict_dir = 'D:\\pycharm\\bishe_tupianfenlei\\pics'
#这个路径下有两个文件，分别是cat和dog
test = os.listdir(predict_dir)
#打印后：['cat', 'dog']
print(test)
#新建一个列表保存预测图片的地址


img = cv2.imread('image_0001.jpg')
img = cv2.resize(img,(32,32),3)
img = img.reshape(1,32,32,3).astype('float')
img /= 255


predict = model.predict_classes(img)
print('识别为：')
print(predict)
predict = int(predict)

print(test[predict])









