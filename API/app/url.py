'''
Author: Dong Xing
Date: 2021-01-17 00:42:44
LastEditors: caly5144 514458959@qq.com
LastEditTime: 2023-11-23 10:14:25
Description: file content
'''
import requests
# import os
# import time
import re
# import sqlite3
import urllib.parse
from typing import Optional
from fastapi import APIRouter,Query, Header
# from fastapi.responses import RedirectResponse, HTMLResponse
from lib.httpcode_dict import HTTP_CODE #,BAIDU_DICT
# from lib.utility import get_tables

router = APIRouter()

# if not os.path.exists('./cache'):
#     os.makedirs('./cache')

# conn = sqlite3.connect('./cache/baidu.db')
# cur = conn.cursor()
# table_list = get_tables(conn)

# if 'baidu' not in table_list:
#     cur.execute("CREATE TABLE baidu(url datatype,status datatype,update_time datatype);")

@router.get("/checkurl/")
async def getHttpStatusCode(u: str = Query(..., min_length=3)):
    try:
        if 'http' not in u:
            u = 'http://'+u
        request = requests.get(u)
        httpStatusCode = request.status_code
        return {'code': httpStatusCode, 'msg': HTTP_CODE[httpStatusCode]}
    except requests.exceptions.HTTPError as e:
        return {'code': 400, 'msg': e}


@router.get("/baidu/")
def get_baidu(u: str = Query(..., min_length=3)):
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'Cache-Control': "max-age=0",
        'Host': "www.baidu.com",
        'Connection': "keep-alive",
        'Content-Type':"application/x-www-form-urlencoded",
        'Referer':"https://www.baidu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    }
    # 网址后缀处理
    if '.' in u[-5:]:
        pass
    elif u[-1] != '/':
        u += '/'
    # 网址协议头处理
    if 'http' in u:
        u = u[u.index('//')+2:]
    if 'www' not in u:
        u = 'www.' + u

    # sql = 'select url,status,update_time from baidu where url like "{}"'.format(u)
    # cur.execute(sql)
    # result = cur.fetchall()
    # if result:
    #     pytime = result[-1][2]
    #     # if time.time() -  pytime < 60:
    #     #     return {'code':result[-1][1],'msg':BAIDU_DICT[result[-1][1]]}
    url = urllib.parse.quote_plus(u)
    baidu = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd='
    search_url = baidu + url
    headers['Referer'] = search_url
    s=requests.Session()
    response = s.get(search_url, headers=headers)
    if response.history:
        print("Request was redirected")
        for resp in response.history:
            url = resp.url            
        response = s.get(url, headers=headers)
    
    text = response.text
    try:
        text = text[:text.index('以下是网页中包含')]
        pattern = re.compile(r'"http://www.baidu.com/link\?url=.+?"')
        result_list = pattern.findall(text)
        if result_list:
            # sql = 'UPDATE baidu SET status = 200,update_time = {} WHERE update_time = {};'.format(time.time(),pytime)
            # # sql = 'INSERT INTO baidu (url,status,update_time) VALUES ({}, {}, {});'.format(repr(u),200,time.time())
            # cur.execute(sql)
            # conn.commit()
            return {'code': 200, 'msg': '该网址已被百度收录！'}
        else:
            return {'code': 403, 'msg': '该网址暂未被百度收录！'}
    except:
        return {'code': 500, 'msg': 'Internet Server Error'}


@router.get("/getua/")
async def get_ua(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}