# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:14:22 2019
        self.
@author: 雁陎
"""

import os
import re
from shutil import copy
from requests import post
from hashlib import sha1
import pymongo
import time

def copyfile(org_path,copy_path):
    current_folder = os.listdir(org_path) # 路径下所有文件组成一个列表
    for file in current_folder:
        if file[-2:] == 'md':
            file_path = org_path+'\\'+ file  # 拼接出要存放的文件夹的路径
            copy(file_path,copy_path) # 将指定的文件file复制到file_dir的文件夹里面

def openmd(org_path,copy_path):  # 替换url链接
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # 连接数据库
    mydb = myclient["mdpicture"]   # 创建数据库
    mycol = mydb["hash_url"]   # 创建集合（数据表）
    pattern = re.compile(r'_v_images/.+\s??=??\d*?x??')
    for file in os.listdir(copy_path):        
        file_path = copy_path+'\\'+ file
        with open(file_path,'r+',encoding = "utf-8") as handler:
             print('正在转化',file,'……')
             content = handler.read()
             handler.seek(0)
             handler.truncate()
             replacelist = pattern.findall(content)
             for each in replacelist:
                 pic_name = each[:int(each.index(r'.')+4)]
                 pic_path = org_path+'\\'+pic_name.replace('/','\\')
                 pic_url = upload(mycol,pic_path,pic_name)
                 if pic_url:
                    content = pattern.sub(pic_url +')',content,count = 1)   
                    # 不知为什么正则替换会把最后一个括号替换掉，所以只能手动加了一个  
             pretext = '---\ntitle:'+file[:-3]+'\ntoc: true\ndate: '\
             +str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))\
             +'\ntags: []\ncategories:  \n-\n---\n\n'
             handler.write(pretext)   # 写文章开头信息
             handler.write(content)
             print(file,"链接已经转化完毕")

def calchash(filepath):  # 计算图片hash值
    with open(filepath,'rb') as f:
        sha1obj = sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        return hash

        
def upload(mycol,pic_path,pic_name): # 上传图片至sm.ms
    url='https://sm.ms/api/upload'
    try:
        file_obj=open(pic_path,'rb')
        file={'smfile':file_obj}	# 参数名称必须为smfile 
        pic_hash = calchash(pic_path)
        # 先检查是否上传过，若无才进行上传
        if mycol.find_one({"hash": pic_hash}):
            print('查询mongodb，图片',pic_name,'已存在')
            result =  mycol.find_one({"hash": pic_hash})['url']       
        else:
            data_result=post(url,data=None,files=file).json()
            if data_result['message'] == 'Upload success.':
                mycol.insert_one({"hash":pic_hash,"url":data_result['data']['url'],"delete":data_result['data']['delete']}) 
                print(' '*4,pic_name,'上传成功，链接为',data_result['data']['url'],'删除链接为',data_result['data']['delete'])
                result =  data_result['data']['url']
            elif data_result['message'][0:21] == 'Image upload repeated':
                print(' '*4,pic_name,'上传失败，图片已存在')	
                result = None	
            else:
                print(' '*4,'其他错误')
                result = None
    except FileNotFoundError:
        print(' '*4,pic_name,'图片未找到，请检查该图是否存在')
        result = None
    return result

def main():
    org_path = r'E:\vnote笔记数据\待转区'  # 原始路径
    copy_path = r'E:\vnote笔记数据\转化完成区'  # 目标路径，原始路径的md会将所有图片转为url后放到这里
    copyfile(org_path,copy_path)
    openmd(org_path,copy_path)


if __name__ == '__main__':
    main()





