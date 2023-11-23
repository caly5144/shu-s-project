'''
Author: Dong Xing
Date: 2021-01-15 20:05:06
LastEditors: Dong Xing
LastEditTime: 2021-01-17 02:58:51
Description: file content
'''
from fastapi import Query,APIRouter,Request
try:
    from qqwry import QQwry

    q = QQwry()
    q.load_file('./data/qqwry.dat')
except:
    print('qqwry导入失败 or qqwry.dat not found')

router = APIRouter()

@router.get("/ipcity/")
async def get_ipcity(ip: str):
    # 数据来源：https://github.com/ipipdotnet/ipdb-php
    result = q.lookup(ip)
    if result:
        return {'code':200,'city':result[0],'operator':result[1]}
    else:
        return {'code':404,'city':None,'operator':None}

@router.get("/ip/")
async def read_root(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}