'''
Author: Dong Xing
Date: 2021-01-14 16:07:51
LastEditors: Dong Xing
LastEditTime: 2021-01-15 22:47:24
Description: API主页
'''
import requests
import re
from typing import List,Optional
from fastapi import FastAPI, Query,Header,Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app_randomacg import read_acg
from httpcode_dict import HTTP_CODE
import ipdb

app = FastAPI(title="雁陎 API")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    html = """
    <html>
        <head>
            <title>雁陎API平台</title>
        </head>
        <body>
            <h1>欢迎使用雁陎API平台！</h1>
            <p>作者博客：<a href="https://sitstars.com">雁陎的自耕地</a></p>
            <p>目前本平台的API有：</p>
            <p><li><a href="/acg/">随机二次元图</a></li></p>
            <p><li><a href="/checkurl/?u=https://www.sitstars.com">检测网址状态</a></li></p>
            <p><li><a href="/baidu/?u=https://www.sitstars.com">查询网址是否被百度收录</a></li></p>
            <p><li><a href="/ipcity/?ip=218.192.3.42">查询ip所在城市</a></li></p>
            <p><li><a href="/ip/">查询访客ip</a></li></p>
        </body>
    </html>
    """
    return html


@app.get("/acg/")
async def return_acg(tand: List[str] = Query(None), tor: List[str] = Query(None),
               m: float = None, n: float = None, seed=None):
    return read_acg(tand, tor, m, n, seed)


@app.get("/checkurl/")
async def getHttpStatusCode(u: str = Query(..., min_length=3)):
    try:
        if 'http' not in u:
            u = 'http://'+u
        request = requests.get(u)
        httpStatusCode = request.status_code
        return {'code': httpStatusCode, 'msg': HTTP_CODE[httpStatusCode]}
    except requests.exceptions.HTTPError as e:
        return {'code': 400, 'msg': e}


@app.get("/baidu/")
async def get_baidu(u: str = Query(..., min_length=3)):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer': 'https://www.baidu.com'
    }
    # 网址后缀处理
    if '.' in u[-5:]:
        pass
    elif u[-1] != '/':
        u += '/'
    # 网址协议头处理
    if ('http' in u) and not ('www' in u):
        u = 'www.' + u[u.index('//')+2:]
    elif ('http' not in u) and not ('www' in u):
        u = 'www.' + u

    baidu = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd='
    search_url = baidu + u
    try:
        response = requests.get(search_url, headers=headers)
        text = response.text
        text = text[:text.index('以下是网页中包含')]
        pattern = re.compile(r'"http://www.baidu.com/link\?url=.+?"')
        result_list = pattern.findall(text)
        if result_list:
            return {'code': 200, 'msg': '该网址已被百度收录！'}
        else:
            return {'code': 403, 'msg': '该网址暂未被百度收录！'}
    except:
        return {'code': 404, 'msg': '百度收录查询失败！'}

@app.get("/getua/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/ipcity/")
async def get_ipcity(ip:str):
    # 数据来源：https://github.com/ipipdotnet/ipdb-php
    db = ipdb.City('./lib/ipipfree.ipdb')
    return db.find_map(str(ip.strip()), "CN")

@app.get("/ip/")
def read_root(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}