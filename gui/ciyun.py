# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:14:22 2019
        self.
@author: 雁陎
"""

from wordcloud import (WordCloud, ImageColorGenerator)
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from random import randint
import jieba

'''
lines=[]
with open('config.txt','r') as handler:
    lines = handler.readlines()

a,b = map(int,lines[3].split(','))  # 颜色h的范围
bgcolor = lines[7].strip('\n').lower()  # 背景颜色
if bgcolor == 'none':
    bgcolor = None
w,h = map(int,lines[9].split(',')) # 云字图尺寸
'''



def generate(colortype,n,m,font,image_path,bgcolor,w,highth,shape,segment_mode,text,maxword):
    
    def color_type(colortype):    # 判断用户选择的颜色模式
        if colortype == '图片颜色':
            random_color = ImageColorGenerator(np.array(Image.open(image_path)))        
            #字体颜色为背景图片的颜色
        else:
            random_color =random_color_func
        return random_color

    def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        h,s,l = randint(n,m),randint(70,100),randint(28,47)
        # h即表示颜色的取值范围，我们可以谷歌colour picker 查看各颜色的取值范围对应的h值
        # 然后在参数中设置 color_func = random_color_func即可令字按照该范围设定颜色
        return "hsl({}, {}%, {}%)".format(h, s, l)
    
    if bgcolor == 'none':
        bgcolor = None
    
    font_dict = {'微软雅黑':r'\msyh.ttc','楷体':r'\simkai.ttf','宋体':r'\simsun.ttc',
             '仿宋':r'\simfang.ttf','隶书':r'\SIMLI.TTF','Times New Roman':r'times.ttf'}
    font_path =  r'C:\Windows\Fonts' + font_dict[font]   # 字体
    
    def shape_judge(w,shape):  # 判断用户选择的形状
        if shape == '方形':
            mask = None
        elif shape == '圆形':
            x,y = np.ogrid[:w,:w]
            mask = 255*((x-w/2) ** 2 + (y-w/2) ** 2 > 4.2*w ** 2).astype(int) 
            # 以(w/2,w/2)为圆心，半径为4.2*w的圆，255不知道干什么的，但是必须有
        else:
            mask = np.array(Image.open(image_path))
        return mask
    
    def segment_words(text):
        article_contents = ""
        #使用jieba进行分词
        words = jieba.cut(text,cut_all=False)
        for word in words:
            #使用空格来分割词，否则词组仍是一起的
            article_contents += word+" "
        return article_contents
            
    def segment_judge(segment_mode,text):
        text=text.lower()
        if segment_mode == '自定义模式':
            return text
        else:
            return segment_words(text)
    
    stopwords = {'.',',','"',':','(',')','.','。','（','）','[',']','”','“','\n','\t',' '}  
    
   
    wordcloud= WordCloud(font_path=font_path, background_color=bgcolor, mode="RGBA", max_words=maxword, 
                         color_func = color_type(colortype),mask= shape_judge(w,shape),width=w, 
                         height=highth,stopwords = stopwords,margin=2).generate(segment_judge(segment_mode,text))
    
    # 你可以通过font path参数来设置字体集
    # width， height， margin可以设置图片属性
    # backgroud_color = "black"，可以设定背景颜色，默认黑色，如果想要设定透明的可以按照上面代码做
    # stopwords 停用词，即云字图中不展示的词组，如各种标点、换行。
    return wordcloud 
    #plt.axis("off")  # 是否绘制坐标轴
    #plt.show()
    #if save_path:
    #wordcloud.to_file('image.png')
    #print('成功生成')
    
