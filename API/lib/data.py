'''
Author: Dong Xing
Date: 2021-01-17 00:50:38
LastEditors: Dong Xing
LastEditTime: 2021-01-17 00:51:37
Description: 数据库模块
'''
###
# todo；
# 根据教程：https://fastapi.tiangolo.com/advanced/async-sql-databases/
# 重构异步数据库
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # 连接数据库
mydb = myclient["mdpicture"]   # 创建数据库
mycol = mydb["acg"]