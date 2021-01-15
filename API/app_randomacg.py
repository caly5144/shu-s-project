'''
Author: Dong Xing
Date: 2021-01-14 22:19:24
LastEditors: Dong Xing
LastEditTime: 2021-01-15 10:50:19
Description: 随机ACG图
'''
from typing import List
from fastapi import Query
from fastapi.responses import RedirectResponse
import pymongo
import random

myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # 连接数据库
mydb = myclient["mdpicture"]   # 创建数据库
mycol = mydb["acg"]


def read_acg(tand: List[str] = Query(None),tor: List[str] = Query(None),
             m: float = None,n:float=None,seed=None):
    condition = []
    seed = random.random()  # 这行代码让每次调用api时能真正返回随机图
    if tand and tor:
        tand = None
    if tand:
        condition.append({'tag': {"$all": tand}})
    if tor:
        condition.append({'tag': {"$in": tor}})
    if n:
        condition.append({'size.wh': {"$gte": n}})
    if m:
        condition.append({'size.wh': {"$lte": m}})
    try:
        result = randomp(condition)
        response = RedirectResponse(url=result)
        response.headers['Content-Security-Policy'] = "Cache-Control: no-cache, must-reva lidate"

    except:
        response = 'null'
    return response


def randomp(condition):
    if condition:
        pipeline = [{'$match': {'$and': []}}, {'$sample': {'size': 1}}]
        pipeline[0]['$match']['$and'].extend(condition)
    else:
        pipeline = [{'$sample': {'size': 1}}]
    data = mycol.aggregate(pipeline)
    for i in data:
        res = i['url']['distribute']+'.jpg'
    return res
