'''
Author: Dong Xing
Date: 2021-01-14 16:07:51
LastEditors: Dong Xing
LastEditTime: 2021-01-17 01:54:03
Description: API主页
'''
from fastapi import FastAPI, Query, Header, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn
from app import acg,ip,url

templates = Jinja2Templates(directory="templates")
app = FastAPI(title="雁陎 API")

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
    }
    return templates.TemplateResponse("index.html", {"request": request,"api_dict": api_dict})


if __name__ == "__main__":
    uvicorn.run(app='main:app',host='0.0.0.0',port=8000,reload=True,proxy_headers=True,forwarded_allow_ips='*')