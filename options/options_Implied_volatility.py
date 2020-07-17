# -*- coding: utf-8 -*-
"""
Created on Sat May 16 02:11:08 2020

@author: 51445
"""

import pandas as pd
import datetime
import tushare as ts
import numpy as np
from math import log,sqrt,exp
from scipy import stats
import plotly.graph_objects as go
import plotly
import plotly.express as px

pro = ts.pro_api()
plotly.offline.init_notebook_mode(connected=True)


def extra_data(date): # 提取数据
    # 提取50ETF合约基础信息
    df_basic = pro.opt_basic(exchange='SSE', fields='ts_code,name,call_put,exercise_price,list_date,delist_date')
    df_basic = df_basic.loc[df_basic['name'].str.contains('50ETF')]
    df_basic = df_basic[(df_basic.list_date<=date)&(df_basic.delist_date>date)] # 提取当天市场上交易的期权合约
    df_basic = df_basic.drop(['name','list_date'],axis=1)
    df_basic['date'] = date

    # 提取日线行情数据
    df_cal = pro.trade_cal(exchange='SSE', cal_date=date, fields = 'cal_date,is_open,pretrade_date')
    if df_cal.iloc[0, 1] == 0:
        date = df_cal.iloc[0, 2] # 判断当天是否为交易日，若否则选择前一个交易日

    opt_list = df_basic['ts_code'].tolist() # 获取50ETF期权合约列表
    df_daily = pro.opt_daily(trade_date=date,exchange = 'SSE',fields='ts_code,trade_date,settle')
    df_daily = df_daily[df_daily['ts_code'].isin(opt_list)]

    # 提取50etf指数数据
    df_50etf = pro.fund_daily(ts_code='510050.SH', trade_date = date,fields = 'close')
    s = df_50etf.iloc[0, 0] 

    # 提取无风险利率数据（用一周shibor利率表示）
    df_shibor = pro.shibor(date = date,fields = '1w')
    rf = df_shibor.iloc[0,0]/100

    # 数据合并
    df = pd.merge(df_basic,df_daily,how='left',on=['ts_code'])
    df['s'] = s
    df['r'] = rf
    df = df.rename(columns={'exercise_price':'k', 'settle':'c'})
    #print(df)
    return df

def data_clear(df): # 数据清洗
    def days(df): # 计算期权到期时间
        start_date = datetime.datetime.strptime(df.date,"%Y%m%d")
        end_date = datetime.datetime.strptime(df.delist_date,"%Y%m%d")
        delta = end_date - start_date
        return int(delta.days)/365

    def iq(df): # 计算隐含分红率
        #q = -log((df.settle+df.exercise_price*exp(-df.interest*df.delta)-df.settle_p)/(df.s0))/df.delta
        q = -log((df.c+df.k*exp(-df.r*df.t)-df.c_p)/(df.s))/df.t
        return q
    
    df['t'] = df.apply(days,axis = 1)
    df = df.drop(['delist_date','date'],axis = 1)

    # 计算隐含分红率
    df_c = df[df['call_put']=='C']
    df_p = df[df['call_put']=='P']
    df_p = df_p.rename(columns={'c':'c_p','ts_code':'ts_code_p',
                         'call_put':'call_put_p'})
    df = pd.merge(df_c,df_p,how='left',on=['trade_date','k','t','r','s'])

    df['q'] = df.apply(iq,axis = 1)
    c_list = [x for x in range(8)]+[11]
    
    df_c = df.iloc[:,c_list]
    df_p = df[['ts_code_p','trade_date','c_p','call_put_p','k','t','r','s','q']]
    df_p = df_p.rename(columns={'c_p':'c','ts_code_p':'ts_code',
                         'call_put_p':'call_put'})
    df_c = df_c.append(df_p)
    #print(df_c)
    return df_c        
    
#根据BS公式计算期权价值
def bsm_value(s,k,t,r,sigma,q,option_type):
    d1 = ( log( s/k ) + ( r -q + 0.5*sigma**2 )*t )/( sigma*sqrt(t) )
    d2 = ( log( s/k ) + ( r -q - 0.5*sigma**2 )*t )/( sigma*sqrt(t) )
    if option_type.lower() == 'c':
        value = (s*exp(-q*t)*stats.norm.cdf( d1) - k*exp( -r*t )*stats.norm.cdf( d2))
    else:
        value = k * exp(-r * t) * stats.norm.cdf(-d2) - s*exp(-q*t) * stats.norm.cdf(-d1)
    return value

#二分法求隐含波动率
def bsm_imp_vol(s,k,t,r,c,q,option_type):
    c_est = 0 # 期权价格估计值
    top = 1  #波动率上限
    floor = 0  #波动率下限
    sigma = ( floor + top )/2 #波动率初始值
    count = 0 # 计数器
    while abs( c - c_est ) > 0.000001:
        c_est = bsm_value(s,k,t,r,sigma,q,option_type) 
        #根据价格判断波动率是被低估还是高估，并对波动率做修正
        count += 1           
        if count > 100: # 时间价值为0的期权是算不出隐含波动率的，因此迭代到一定次数就不再迭代了
            sigma = 0
            break
        
        if c - c_est > 0: #f(x)>0
            floor = sigma
            sigma = ( sigma + top )/2
        else:
            top = sigma
            sigma = ( sigma + floor )/2
    return sigma  

def cal_iv(df): # 计算主程序
    option_list = df.ts_code.tolist()

    df = df.set_index('ts_code')
    alist = []

    for option in option_list:
        s = df.loc[option,'s']
        k = df.loc[option,'k']
        t = df.loc[option,'t']
        r = df.loc[option,'r']
        c = df.loc[option,'c']
        q = df.loc[option,'q']
        option_type = df.loc[option,'call_put']
        sigma = bsm_imp_vol(s,k,t,r,c,q,option_type)
        alist.append(sigma)
    df['iv'] = alist
    return df  
 
def data_pivot(df): # 数据透视
    df = df.reset_index()
    option_type = 'C' # 具有相同执行价格、相同剩余到期时间的看涨看跌期权隐含波动率相等，因此算一个就够了
    df = df[df['call_put']==option_type]
    df = df.drop(['ts_code','trade_date','c','s','r','call_put','q'],axis=1)
    df['t'] = df['t']*365
    df['t'] = df['t'].astype(int)
    df = df.pivot_table(index=["k"],columns=["t"],values=["iv"])
    df = df.reset_index()
    df.to_excel(r'iv.xlsx')
    print('数据保存成功，请进行修改')

def fitting(df): # 多项式拟合    
    col_list = df.columns
    for i in range(df.shape[1]-1):
        x_col = col_list[0]
        y_col = col_list[i+1]
        df1 = df.dropna(subset=[y_col])
        
        x = df1.iloc[:,0]
        y = df1.iloc[:,i+1]

        degree = 2
                
        weights = np.polyfit(x, y, degree)
        model = np.poly1d(weights)
        predict = np.poly1d(model)
        x_given_list = df[pd.isnull(df[y_col]) == True][x_col].tolist()
        # 所有空值对应的k组成列表
        for x_given in x_given_list:
            y_predict = predict(x_given)
            df.loc[df[x_col]==x_given, y_col] = y_predict
    return df

def plot_df(): # 作图时进行的数据清洗
    df = pd.read_excel('iv.xlsx',skiprows= 1)
    df = df.dropna(subset=['t'])
    df = df.drop(['t'],axis = 1)
    df = df.rename(columns={'Unnamed: 1':'k'})
    return df

def im_surface(): # 波动率曲面作图
    df = plot_df()
    df = fitting(df)    
    #df.to_excel('iv_fitting.xlsx')
    df = df.set_index('k')

    y = np.array(df.index)
    x = np.array(df.columns)
    fig = go.Figure(data=[go.Surface(z=df.values, x=x, y=y)])

    fig.update_layout(scene = dict(
                    xaxis_title='剩余期限',
                    yaxis_title='执行价格',
                    zaxis_title='隐含波动率'),
                    width=1400,
                    margin=dict(r=20, b=10, l=10, t=10))
    #fig.write_image("fig1.jpg")
    plotly.offline.plot(fig)

def smile_plot(): # 波动率微笑作图
    df = plot_df()
    df = df.set_index('k')
    df = df.stack().reset_index()
    df.columns = ['k', 'days', 'iv']
    fig = px.line(df, x="k", y="iv", color="days",line_shape="spline")
    plotly.offline.plot(fig)

def main():
    date = '20200515'
    df = extra_data(date) # 提取数据
    df = data_clear(df) # 数据清洗
    df = cal_iv(df) # 计算隐含波动率
    data_pivot(df) # 数据透视表
    smile_plot() # 波动率微笑
    im_surface() # 波动率曲面
    
if __name__ == '__main__':
    main()
