'''
Author: Dong Xing
Date: 2021-01-14 22:19:24
LastEditors: caly5144 514458959@qq.com
LastEditTime: 2023-11-23 11:28:28
Description: 随机ACG图
'''
from typing import List
from fastapi import Query,APIRouter,Request
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
import random

try:
    from lib.data import mycol
except:
    print('mongo数据库配置错误')

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/acg_test/",response_class=HTMLResponse)
def random_acg_test(request: Request,tand: List[str] = Query(None),tor: List[str] = Query(None),
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
    
    # try:
    result = randomp(condition)
    return templates.TemplateResponse("img.html", {"request": request,"url": result})
    # response = RedirectResponse(url=result)
    # response.headers['Content-Security-Policy'] = "Cache-Control: no-cache, must-reva lidate"

    # except:
    #     response = 'null'
    # return response

@router.get("/acg/")
def random_acg(tand: List[str] = Query(None),tor: List[str] = Query(None),
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