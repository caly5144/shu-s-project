'''
Author: Dong Xing
Date: 2021-01-17 00:38:53
LastEditors: caly5144 514458959@qq.com
LastEditTime: 2023-11-23 13:34:53
Description: 公共模块
'''

import inspect
import requests
import base64
from io import BytesIO

import asyncio
from functools import wraps

def timeout_decorator(seconds: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                return {
                    'code': 504,
                    'msg': '请求超时'
                }
        return wrapper
    return decorator

def get_tables(conn,dbtype='sqlite'):  # 获取所有表名
    '''
    传入sqlite3 connect
    返回列表
    '''
    cur = conn.cursor()
    if dbtype == 'sqlite':
        cur.execute(
            "select name from sqlite_master where type='table' order by name")
    else:
        cur.execute('SHOW TABLES')
    alist = cur.fetchall()
    result = [x[0] for x in alist]
    return result

def get_bing_img_url():
    response = requests.get('http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1')
    data = response.json()
    imgurl = 'http://cn.bing.com' + data['images'][0]['url']
    if '&rf=' in imgurl:
        imgurl = imgurl[:imgurl.index('&rf=')]
    return imgurl

def img_to_base64(imgurl):
    '''将图片链接转换为base64编码'''
    response = requests.get(imgurl)
    img = BytesIO(response.content)
    return 'data:image/png;base64,' + base64.b64encode(img.getvalue()).decode()

def get_function_default_args(func):
    '''获取函数默认参数'''
    sign = inspect.signature(func)
    return {
        k: v.default
        for k, v in sign.parameters.items()
        if v.default is not inspect.Parameter.empty
    }