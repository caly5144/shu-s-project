# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:40:28 2020

@author: 雁陎
"""

import pandas as pd
import sqlite3
import datetime
import plotly_express as px
import plotly
plotly.offline.init_notebook_mode(connected=True)

def get_data(): # 获取数据
    conn = sqlite3.connect(r'E:\sqlite3\nCoV\nCoV.db')
    url = 'https://cdn.jsdelivr.net/gh/canghailan/Wuhan-2019-nCoV/Wuhan-2019-nCoV.csv'
    df = pd.read_csv(url)
    
    df['now'] = df.confirmed-df.cured-df.dead # 添加一列，现存确诊
    df['region_class'] = 0
    df.loc[pd.isnull(df.province) == False , 'region_class' ] = 1
    df.loc[pd.isnull(df.city) == False , 'region_class' ] = 2
    # 添加一列region_class，判断行政级别
    
    df = df.set_index('date')
    df.to_sql('data',conn,if_exists='replace')

def data_clear():
    conn = sqlite3.connect(r'E:\sqlite3\nCoV\nCoV.db')
    region_dict = {0:'country',1:'province',2:'city'}
    for region_class in range(3):            
        df = pd.read_sql('select * from data where {0} like {1}'\
                         .format('region_class',region_class),conn)
        item_list = [('confirmed','inc_confirmed'),('suspected','inc_suspected')
        ,('cured','inc_cured'),('dead','inc_dead')]
        
        for index in range(4):
            df['temp'] = df.groupby(region_dict[region_class])\
            [item_list[index][0]].shift(1) # 添加一列        
            df['temp'].fillna(0, inplace=True) # 缺失值（即疫情第一天），填充0
            df[item_list[index][1]] = df[item_list[index][0]] - df['temp']
            df = df.drop(['temp'],axis=1) 
    
        df = df.set_index('date')
        df.to_sql(region_dict[region_class],conn,if_exists='replace')
        print(region_dict[region_class],'已添加到数据库中')

def table_exist(conn,table): # 判断某表是否存在
    cursor = conn.cursor()
    cursor.execute("select name from sqlite_master where type='table'")
    alist = cursor.fetchall()
    alist = [num for elem in alist for num in elem] 
    return (table in alist)

def pop_clear(): # 人口数据存储与清洗
    conn = sqlite3.connect(r'E:\sqlite3\nCoV\nCoV.db')
    cursor = conn.cursor() # 获取一个光标
    if table_exist(conn,'pop'):
        df = pd.read_sql('select * from pop',conn)
        
    else:
        df = pd.read_excel('population.xls',skiprows= 3)
        col_n = ['Country Name','2018']
        df = pd.DataFrame(df,columns = col_n) # 选取其中两列数据
        df.rename(columns={'Country Name':'country', '2018':'pop'}, inplace = True)
        df = df.set_index('country')        
        df.to_sql('pop',conn,if_exists='replace')
        print('人口数据储存成功')    
    df = df.reset_index()
    country_list = df['country'].to_list() # 获取population中所有国家列表   
    # 获取数据库中已经存在的国家列表
    country_ncov = cursor.execute('SELECT {0} FROM {0}'.format("country")).fetchall()
    country_ncov = set([elem for item in country_ncov for elem in item])
    
    # 数据清洗主程序
    def process(df):
        add_serie = [['法属圭亚那',289763],['圣巴泰勒米',9868],['马提尼克',375554],['马约特',270400],
                     ['梵蒂冈',1000],['格恩西岛',67052],['荷属安的列斯',227000],['巴勒斯坦',5052000],
                     ['留尼汪',860000],['泽西岛',106800],['瓜德罗普',400104],['钻石公主号邮轮',3700],
                     ['美属维尔京群岛',107300],['蒙特塞拉特',5215],['英属维尔京群岛',30191],['圣皮埃尔和密克隆',5800],
                     ['福克兰群岛（马尔维纳斯）',3459],['安圭拉',16290],]
        
        col_n = ['country','pop']
        df = df.append(pd.DataFrame(add_serie, columns=col_n))
        
          
        mapping_dict = {"country":{"俄罗斯联邦": "俄罗斯","多米尼加共和国": "多米尼加",
                                        "阿拉伯埃及共和国":"埃及","斯洛伐克共和国":"斯洛伐克",
                                        "圣马丁（法属）":"圣马丁","波斯尼亚和黑塞哥维那":"波黑",
                                        "毛里塔尼亚":"毛利塔尼亚","大韩民国":"韩国",
                                        "捷克共和国":"捷克","阿拉伯联合酋长国":"阿联酋",
                                        "文莱达鲁萨兰国":"文莱","伊朗伊斯兰共和国":"伊朗",
                                        "中非共和国":"中非","委内瑞拉玻利瓦尔共和国":"委内瑞拉",
                                        "安道尔共和国":"安道尔","马恩岛":"英国属地曼岛",
                                        "几内亚比绍共和国":"几内亚比绍","也门共和国":"也门",
                                        "特克斯科斯群岛":"特克斯和凯科斯群岛","阿拉伯叙利亚共和国":"叙利亚",
                                        "北马里亚纳群岛":"北马里亚纳"}} 
        df = df.replace(mapping_dict)  # 国家名替换
        df.drop_duplicates(['country'],keep = "first") # 多次运行会有重复数据，需要进行清洗
        df = df.set_index('country')
        return df
    
    
    alist = [i for i in country_ncov if i not in country_list]
    if alist:
        print('尝试清洗人口数据……')
        df = process(df)
        alist = [i for i in country_ncov if i not in set(df.index.to_list())]
        if alist:
            print('已进行过初步清洗，但仍然存在国家名不一致的情况，修改代码后请再次运行：{0}'.format(alist))
        else:
            print('清洗完毕')
    else:
        print('未发现有国家名不一致的情况，无需清洗')
    df = df.set_index('country')
    df.to_sql('pop',conn,if_exists='replace')

def country_ratio(): # 各种比率
    conn = sqlite3.connect(r'E:\sqlite3\nCoV\nCoV.db')
    pop = pd.read_sql('select * from pop',conn)
    infect = pd.read_sql('select * from country',conn)
    df = pd.merge(infect, pop, how='left', on='country')
    df = df.set_index('date')
    df['pop'] = df['pop'].astype(float)
    df['inf_ratio'] = df['confirmed']/df['pop']*10000 # 万人感染率
    df['death_ratio'] = df['dead']/df['confirmed'] # 粗死亡率
    df['cure_ratio'] = df['cured']/df['confirmed'] # 治愈率
    df['death_ratio_x'] = df['dead']/(df['dead']+df['cured']) # 细死亡率
    
    df.to_sql('country_ratio',conn,if_exists='replace')
    print('最终清洗数据已存入至数据库中')

def type_trans(elem_list,elem):
    if type(elem) == str:
        elem_list.append(elem)
    elif type(elem) in [list,tuple,set]:
        elem_list.extend(elem)        
    else:
        elem_list = None
    return elem_list

def select(data=datetime.date.today().strftime('%Y-%m-%d'),item = ['confirmed','dead'],
           sort_item = ['confirmed'],condition = '',head_row = 20,is_exp = False):
    
    if set(sort_item)-set(item):
        print('分类参数中有多余的参数')        
    else:
        item_list = ['date','country']
        sort_item_list = []
        item_list = type_trans(item_list,item)
        sort_item_list = type_trans(sort_item_list,sort_item)
        if item_list and sort_item_list:            
            conn = sqlite3.connect(r'E:\sqlite3\nCoV\nCoV.db')
            if condition:
                df = pd.read_sql('select {0} from country_ratio where {1}'\
                                 .format(','.join(item_list),condition),conn)
            else:
                df = pd.read_sql('select {0} from country_ratio'\
                                 .format(','.join(item_list)),conn)
            
            if data[0:2]=='20':
                selected = df[df['date'] ==data].sort_values(by = sort_item,ascending = False)
            else:
                selected = df[df['country'] ==data].sort_values(by = 'date',ascending = False)
            
            if is_exp:
                file_name = '{0}_{1}.xlsx'.format(data,''.join(item))
                selected.to_excel(file_name)
                print('{0}数据导出成功'.format(file_name))
            else:
                print(selected.head(head_row))
        else:
            print('参数类型输入错误，请重新输入')
            selected = pd.DataFrame()
    return selected

def select_control(country_list = ['中国'],item_list = ['inc_confirmed'],head_row = 20,is_exp = False): # 对照组统计
    conn = sqlite3.connect(r'E:\sqlite3\nCoV\nCoV.db')
    tran = {"confirmed":"累计确诊","suspected":"疑似","dead":"累计死亡",
            "cured":"累计治愈","now":"现存确诊","inc_confirmed":"新增确诊",
            "inc_suspected":"新增疑似","inc_cured":"新增治愈","inc_dead":"新增死亡"}
    df = pd.read_sql('select * from country_ratio',conn)
    df = df.set_index('date')
    df_sum = df[item_list].groupby('date').sum()
    df_fin = pd.DataFrame()
    for item in item_list:
        for country in country_list:        
            df_fin[country+tran[item]] = df[df['country'] == country][item]
        df_fin['其他'+tran[item]] = df_sum[item] - \
        df[df['country'].isin(country_list)][item].groupby('date').sum()
        df_fin['总计'+tran[item]] = df_sum[item]
    df_fin = df_fin.sort_values(by = 'date',ascending = False).head(head_row) 
    if is_exp:
        file_name = '{0}_{1}.xlsx'.format(''.join(country_list),''.join(item_list))
        df_fin.to_excel(file_name)
        print('{0}数据导出成功'.format(file_name))
    else:
        print(df_fin.head(head_row))
            
def report(): # 尚未编写完成
    df_country = select('中国',['confirmed','death_ratio','death_ratio_x'])
    pic = px.scatter(df_country, x='confirmed', y='death_ratio')


def main():
    
    #get_data()
    #data_clear()
    #pop_clear()
    #country_ratio()   
    #report()
    select('丹麦',['confirmed','dead','death_ratio_x'])
    #select('2020-04-18',item = ['confirmed','inf_ratio'],sort_item=['inf_ratio'],condition = 'pop>1000000 and confirmed>1000')
    #select_control(['意大利','西班牙'],['inc_confirmed'],is_exp = True)  

if __name__ == '__main__':
    main()