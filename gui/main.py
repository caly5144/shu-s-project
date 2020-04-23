# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 00:59:08 2020

@author: 51445
"""


import PySimpleGUI as sg     
import sys
import os

program_path = os.getcwd()
cache_path = program_path+r'\cache'

def main_gui(): # 程序主界面    
    if os.path.exists(cache_path) == False:
        os.makedirs(cache_path)
    
    frame_layout_file = [[sg.Button('批量重命名',key='mr')]]
    frame_layout_anay = [[sg.Button('词云图生成',key='cy')]]
    layout = [[ sg.Text('欢迎使用雁陎工具箱'),],
          [sg.Frame(layout = frame_layout_file, title='文件处理', relief=sg.RELIEF_SUNKEN)],
          [sg.Frame(layout = frame_layout_anay, title='分析工具', relief=sg.RELIEF_SUNKEN)],
          [sg.Button('退出程序')]]

    win_main = sg.Window('雁陎的工具箱', layout,font=("宋体", 15),default_element_size=(100,1)) 
    while True:
        ev_main, vals_main = win_main.Read()
        if ev_main in (None,'退出程序'):
            break
        if ev_main == 'mr':
            mult_rename_gui(win_main)
        if ev_main == 'cy':
            ciyun_gui(win_main)
            
    win_main.close()

def mult_rename_gui(win_main): # 批量重命名GUI
    import mult_rename as mr 
    win_main.Hide()
    layout_mr = [
                [sg.FolderBrowse('打开文件夹',key='folder',target='mr_text1'),sg.Combo(['重命名为hash值', 'choice 2'],key='choice',size=(15,1),default_value='重命名为hash值'),sg.Button('重命名'),sg.Button('返回工具箱',key='back_mr')],
                [sg.Text('你选择的文件夹是:',font=("宋体", 10)),sg.Text('',key='mr_text1',size=(50,1),font=("宋体", 10))],
                [sg.Text('程序运行记录',justification='center')],
                [sg.Output(size=(70, 20),font=("宋体", 10))]                                
                ] 

    win_mr = sg.Window('批量重命名', layout_mr,font=("宋体", 15),default_element_size=(50,1))
    while True:
        ev_mr, vals_mr = win_mr.Read()
        if ev_mr is None or ev_mr == 'back_mr':
            win_mr.close()
            win_main.UnHide()
            sys.modules.pop('mult_rename') # 释放已导入模块
            break
        if vals_mr['folder']:
            if vals_mr['choice'] == '重命名为hash值':
                print('您选择的模式为hash值+后缀')
                print('{0}正在重命名原文件为hash值{0}'.format('*'*10))
                mr.mult_rename(vals_mr['folder'])
                print('{0}重命名完毕{0}'.format('*'*10))
            else:
                print('请选择一个重命名模式')
        else:
            print('请先选择文件夹')


def ciyun_gui(win_main): # 词云图生成GUI
    import ciyun as cy
    win_main.Hide()
    layout_c = [
                [sg.Text('字体颜色范围：',key='font_color_range'),sg.Text('最小值',key='min'),sg.Spin([i for i in range(1,360)], initial_value=190,key='min_select'),sg.Text('最大值',key='max'),sg.Spin([i for i in range(1,360)], initial_value=250,key='max_select')],                
                [sg.InputText('关于字体颜色范围取值（H），可以参考https://www.webfx.com/web-design/color-picker/',key='font_color_range_p',disabled=True)],
                [sg.Text('词云图形状：',key='shape'),sg.Combo(['方形', '圆形','图片形状'],key='shape_select',default_value='图片形状',enable_events=True,size=(8,1))],
                ]
    layout_d = [[sg.FileBrowse('打开图片',key='filebrowser',target='image_shape'),sg.InputText('',key='image_shape',disabled=True)]]
    
    layout = [  
                [sg.Text('字体颜色模式：',key='font_color_type'),sg.Combo(['图片颜色', '自定义颜色'],key='font_color_type_select',default_value='自定义颜色',size=(12,1),enable_events=True)],
                [sg.Text('即是按照给定图片的颜色给字上色还是自定义字体颜色',key='font_color_type_p')],                
                [sg.Column(layout_c,key='is_visible')],
                [sg.Column(layout_d,key='open_image')],
                [sg.Text('词云图尺寸：',key='size'),sg.Text('宽',key='width'),sg.Spin([i for i in range(1,2001)], initial_value=1000,key='width_select'),sg.Text('高',key='highth'),sg.Spin([i for i in range(1,2001)], initial_value=800,key='higth_select')],                 
                [sg.Text('字体：',key='font'),sg.Combo(['微软雅黑','楷体','宋体','仿宋','隶书','Times New Roman'],key='font_select',default_value='微软雅黑')],
                [sg.Text('背景颜色：',key='back_color'),sg.ColorChooserButton('颜色选择',key='back_color_select'),sg.Button('透明色点我',key='color_none') ] ,                                       
                [sg.Text('分词模式：',key='word_split_type'),sg.Combo(['自定义模式', '自动分词模式'],key='word_split_type_select',default_value='自动分词模式',size=(8,1))],
                [sg.Text('注：自定义模式即按照你所给的词组进行绘制，词组之间用空格分隔\n自动分词模式即给定一段话，程序自动进行分词并按照频率进行绘制')],
                [sg.Text('最大词数：',key='max_words'),sg.Spin([i for i in range(1,5001)], initial_value=1000,key='max_words_select'),sg.Text('词云图上显示的词数量，退格键删除有问题，建议delete键')],
                [sg.Text('输\n入\n文\n本'),sg.Multiline(size=(30, 10),font=("宋体", 10),key='inputtext'),sg.Text('程\n序\n运\n行\n记\n录'),sg.Output(size=(30, 10),font=("宋体", 10))],
                [sg.FolderBrowse('保存路径',key='folderbrowser',enable_events=True,target='backup'),sg.InputText('wordcloud.png',key='savefile_name',enable_events=True,size=(15,1)),sg.InputText('',key='file_path',disabled=True,size=(40,1))],
                [sg.Button('开始生成！',key='generate'),sg.Button('保存图片',key='saveas'),sg.Button('返回工具箱',key='back'),sg.Text('',key='backup',visible=False)]                               
                ] 

    window = sg.Window('词云图生成', layout,font=("宋体", 12),default_element_size=(50,1))
    while True:
        event, values = window.Read()
        if event in (None,'back'):
            window.close()
            win_main.UnHide()
            sys.modules.pop('ciyun') # 释放已导入模块
            break
        
        if event == 'font_color_type_select': # 判断字体颜色模式并隐藏相应控件
            if values['font_color_type_select'] == '图片颜色':
                window['shape_select'].Update('图片形状')
                window['is_visible'].Update(visible=False)
            else:
                window['is_visible'].Update(visible=True)  
        
        if event == 'shape_select': # 判断形状模式并决定是否隐藏打开文件控件
            if values['shape_select']=='图片形状':
                window['open_image'].Update(visible=True)
            else:
                window['open_image'].Update(visible=False)
        bgcolor = 'none' 
        if event == 'color_none': # 判断是否选择透明背景色
            bgcolor = 'none'
        if event == 'color_none':    
            bgcolor = values['back_color_select']
            
        if event == 'generate':
            color_type = values['font_color_type_select']
            if color_type == '图片颜色':
                n,m=(0,0)
            else:
                n = min(values['min_select'],values['max_select'])
                m = max(values['min_select'],values['max_select'])
            font = values['font_select']
            
            w,h = (values['width_select'],values['higth_select'])
            shape = values['shape_select']
            if shape =='图片形状':
                image_path = values['filebrowser']
            else:
                image_path = ''
            segment_mode = values['word_split_type_select']
            text = values['inputtext']
            maxword = values['max_words_select']
            wordcloud = cy.generate(color_type,n,m,font,image_path,bgcolor,w,h,shape,segment_mode,text,maxword)
            wordcloud.to_file('cache\image.png')
            image_view('cache\image.png')
            print('词云图生成成功')
        if event in ('folderbrowser','savefile_name','saveas'):
            window['file_path'].update(values['folderbrowser']+'/'+values['savefile_name'])
        
        if event == 'saveas': 
            print(values['file_path'])
            try:
                wordcloud.to_file(values['file_path'])
                print('词云图保存成功')
            except:
                print('你还没有生成相应的词云图')

def image_view(pic_path): # 图片查看器
    layout = [
                [sg.Image(pic_path, key="imageview")]
    ]
    inputWindow = sg.Window("图片查看器",layout)
    while True:
        event, values = inputWindow.Read()
        if event in (None,'关闭'):
            break
    inputWindow.close()

def main():    
    main_gui()
    #image_view(r'E:\python\gui\image.png')

if __name__ == '__main__':
    main()            
            
