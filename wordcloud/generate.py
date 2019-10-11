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

lines=[]
with open('config.txt','r') as handler:
    lines = handler.readlines()

a,b = map(int,lines[3].split(','))  # 颜色h的范围
bgcolor = lines[7].strip('\n').lower()  # 背景颜色
if bgcolor == 'none':
    bgcolor = None
w,h = map(int,lines[9].split(',')) # 云字图尺寸


def font_select():
    font_input = lines[5].strip('\n')
    font_dict = {'微软雅黑':r'\msyh.ttc','楷体':r'\simkai.ttf','宋体':r'\simsun.ttc',
             '仿宋':r'\simfang.ttf','隶书':r'\SIMLI.TTF','Times New Roman':r'times.ttf'}
    return r'C:\Windows\Fonts' + font_dict[font_input]   # 字体


def shape_judge():  # 判断用户选择的形状
    cloud_shape = lines[11].strip('\n').lower()  # 云字图形状
    if cloud_shape == 'rectangle':
        mask = None
    elif cloud_shape == 'round':
        x,y = np.ogrid[:w,:w]
        mask = 255*((x-w/2) ** 2 + (y-w/2) ** 2 > 4.2*w ** 2).astype(int) 
        # 以(w/2,w/2)为圆心，半径为4.2*w的圆，255不知道干什么的，但是必须有
    else:
        mask = np.array(Image.open(r"shape.jpg"))
    return mask

def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h,s,l = randint(a,b),randint(70,100),randint(28,47)
        # h即表示颜色的取值范围，我们可以谷歌colour picker 查看各颜色的取值范围对应的h值
        # 然后在参数中设置 color_func = random_color_func即可令字按照该范围设定颜色
    return "hsl({}, {}%, {}%)".format(h, s, l)

def color_judge():   
    font_color_input = int(lines[1].strip('\n'))
    if font_color_input == 1:
        random_color = ImageColorGenerator(np.array(Image.open(r"shape.jpg")))        
        #字体颜色为背景图片的颜色
    else:
        random_color =random_color_func
    return random_color
    
def segment_words(text):
    article_contents = ""
    #使用jieba进行分词
    words = jieba.cut(text,cut_all=False)
    for word in words:
        #使用空格来分割词，否则词组仍是一起的
        article_contents += word+" "
    return article_contents
        
def segment_judge():
    segment_mode = int(lines[13].strip('\n'))
    text=open(u'word.txt','r').read().lower()
    if segment_mode == 1:
        return text
    else:
        return segment_words(text)

stopwords = {'.',',','"',':','(',')','.','。','（','）','[',']','”','“','\n','\t',' '}

charnum = int(lines[15].strip('\n'))

wordcloud= WordCloud(font_path=font_select(), background_color=bgcolor, mode="RGBA", max_words=charnum, 
                     color_func = color_judge(),mask= shape_judge(),width=w, 
                     height=h,stopwords = stopwords,margin=2).generate(segment_judge())

# 你可以通过font path参数来设置字体集
# width， height， margin可以设置图片属性
# backgroud_color = "black"，可以设定背景颜色，默认黑色，如果想要设定透明的可以按照上面代码做
# stopwords 停用词，即云字图中不展示的词组，如各种标点、换行。
 
plt.axis("off")  # 是否绘制坐标轴
plt.show()
wordcloud.to_file('wordcloud.png')
print('词云图已生成')
