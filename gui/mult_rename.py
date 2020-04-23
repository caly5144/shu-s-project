# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 01:38:18 2020

@author: 51445
"""

from hashlib import sha1
import os,shutil

def calchash(file_path):  # 计算图片hash值
    with open(file_path,'rb') as f:
        sha1obj = sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        return hash
 
    
def mult_rename(dir_path): # 批量重命名
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path,file)
        if not os.path.isdir(file_path): # 判断是否为文件夹           
            pic_hash = calchash(file_path)      # 计算hash值             
            last = file[file.rindex(r'.'):]  # 后缀
            new_name = pic_hash+last
            if file == new_name:
                print(file,'无需修改')
            else:
                try:
                    new_path = os.path.join(dir_path,new_name)
                    os.rename(file_path,new_path)
                    print('{0}已重命名为{1}'.format(file,new_name))
                except FileExistsError:
                    repeat_path = dir_path+r'\重复文件夹'
                    if os.path.exists(repeat_path) == False:
                        os.makedirs(repeat_path)
                    new_path = os.path.join(repeat_path,new_name)
                    shutil.move(file_path,new_path)
                    print(r'{0}文件重复，已移至重复文件夹下'.format(file))