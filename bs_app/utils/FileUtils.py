import os
import zipfile
import re

# 解压zip文件 返回文件名字不带后缀
def unzip(path,mp):
    z = zipfile.ZipFile(mp)
    for name in z.namelist()[1:]:
        z.extract(name, path=path)
        m = re.match(r'[A-Za-z0-9]+', name)
    z.close()
    return m


# 得到目录一个目录最后的文件名
def get_last_filename(name):

    result = re.findall(r'[^\\/:*?"<>|\r\n]+$', name)
    return result[0]

# 查看当前目录下是否有同名文件 若有则创建一个新的 不覆盖
def check_filename_available(filename):
    n = [0]

    def check_meta(file_name):
        file_name_new = file_name
        if os.path.isfile(file_name):
            file_name_new = file_name[:file_name.rfind('.')]+'_'+str(n[0])+file_name[file_name.rfind('.'):]
            n[0] += 1
        if os.path.isfile(file_name_new):
            file_name_new = check_meta(file_name)
        return file_name_new
    return_name = check_meta(filename)
    return return_name
