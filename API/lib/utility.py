'''
Author: Dong Xing
Date: 2021-01-17 00:38:53
LastEditors: Dong Xing
LastEditTime: 2021-01-17 00:39:31
Description: 公共模块
'''

def get_tables(conn,dbtype='sqlite'):  # 获取所有表名
    '''
    传入sqlite3 connect
    返回列表
    '''
    cur = conn.cursor()
    if dbtype == 'sqlite':
        cur.execute(
            "select name from sqlite_master where type='table' order by name")
    else:
        cur.execute('SHOW TABLES')
    alist = cur.fetchall()
    result = [x[0] for x in alist]
    return result