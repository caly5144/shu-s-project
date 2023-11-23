'''
Author: Dong Xing
Date: 2021-01-14 16:07:51
LastEditors: caly5144 514458959@qq.com
LastEditTime: 2023-11-23 14:39:33
Description: API主页
'''
from fastapi import applications
from fastapi import FastAPI, Query, Header, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
import uvicorn
from app import acg, ip, url, bing_img
from lib.utility import get_function_default_args

templates = Jinja2Templates(directory="templates")
app = FastAPI(title="雁陎 API")
REQUEST_TIMEOUT_ERROR = 1 # 请求超时时间

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.sitstars.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(acg.router)
app.include_router(ip.router)
app.include_router(url.router)
app.include_router(bing_img.router)

def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    param_dict = get_function_default_args(get_swagger_ui_html)
    swagger_js_url = param_dict['swagger_js_url'].replace('https://cdn.jsdelivr.net/npm/', 'https://unpkg.com/')
    swagger_css_url = param_dict['swagger_css_url'].replace('https://cdn.jsdelivr.net/npm/', 'https://unpkg.com/')
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url=swagger_js_url,
        swagger_css_url=swagger_css_url
    )

def swagger_monkey_patch_redoc(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    param_dict = get_function_default_args(get_redoc_html)
    redoc_js_url = param_dict['redoc_js_url'].replace('https://cdn.jsdelivr.net/npm/', 'https://unpkg.com/')
    return get_redoc_html(
        *args, **kwargs,
        redoc_js_url=redoc_js_url,
    )

applications.get_swagger_ui_html  = swagger_monkey_patch
applications.get_redoc_html = swagger_monkey_patch_redoc

@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    api_dict = {
        "acg":{
            "url": "/acg_test/",
            "name": "随机二次元图"
        },
        "check_url":{
            "url":"/checkurl/?u=https://www.sitstars.com",
            "name":"检测网址状态"
        },
        "baidu":{
            "url":"/baidu/?u=https://www.sitstars.com",
            "name":"查询网址是否被百度收录"
        },
        "ipcity":{
            "url":"/ipcity/?ip=218.192.3.42",
            "name":"查询ip所在城市"
        },
        "ip":{
            "url":"/ip/",
            "name":"查询访客ip"
        },
        "getua":{
            "url":"/getua/",
            "name":"查询访客UA"
        },
        "bing_img":{
            "url":"/bing_img/",
            "name":"获取每日bing壁纸"
        },
    }
    return templates.TemplateResponse("index.html", {"request": request,"api_dict": api_dict})


if __name__ == "__main__":
    uvicorn.run(app='main:app',host='0.0.0.0',port=8000,reload=True,proxy_headers=True,forwarded_allow_ips='*')