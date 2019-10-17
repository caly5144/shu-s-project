# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:10:12 2019

@author: 雁陎
"""


import requests
import base64

import urllib
import json

from PIL import Image, ImageGrab
from pynput.keyboard import Key,Controller,Listener

import time


client_id ='填入你的API Key'
client_secret ='填入你的Secret Key'
#获取token
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key

def ocr(image_data):  # ocr识别函数
    base64_ima = base64.b64encode(image_data)
    access_token=get_token()
    data = {
            'image': base64_ima
            }
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + str(access_token)
    result = requests.post(url, params=headers, data=data).json()
    for word in result['words_result']:
        yield word['words']


def on_press(key):
    pass    
    # print('{0} pressed'.format(key))

def on_release(key):
    # print('{0} release'.format(key))
    keyboard = Controller()
    if key ==  Key.f7:
        keyboard.press(Key.cmd)
        keyboard.press(Key.shift)
        keyboard.press('s')
        keyboard.release(Key.shift)
        keyboard.release(Key.cmd)
        keyboard.release('s')
        time.sleep(2)
        pic = ImageGrab.grabclipboard()
        if isinstance(pic, Image.Image):
            pic.save('testpic.png')
        with open("testpic.png", 'rb') as f:
            image_data = f.read()                
        words = ocr(image_data)
        for word in words:
            print(word)
    if key == Key.esc:        
        # Stop listener
        return False #停止监视

def main():
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
 

        