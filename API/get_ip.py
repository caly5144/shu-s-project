'''
Author: Dong Xing
Date: 2021-01-15 20:05:06
LastEditors: Dong Xing
LastEditTime: 2021-01-15 20:13:32
Description: file content
'''
import ipdb
path='./lib/ipipfree.ipdb'
db = ipdb.City(path)
# file_w=open(path+'/content.txt','w',encoding='utf-8')         #记录已解析的ip+location
# file_w_01=open(path+'/content01.txt','w',encoding='utf-8')  #记录未能解析的ip
ip = '218.192.3.42'
city=db.find_map(str(ip.strip()), "CN")
print(city)