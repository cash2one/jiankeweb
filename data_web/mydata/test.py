# -*- coding:utf-8 -*-

import threading

import pymssql
from sqlalchemy import create_engine, exc
import pandas as pd

CONN_77 = pymssql.connect(
        server='172.16.240.77',
        user='Lily',
        password='Lily123',
        database='BigData_CRM',
)


class DataApi(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self)
        self.threadname = threadname
        self.connect = create_engine('mysql+mysqldb://root:jianke@123@172.17.240.5:3306/data_play?charset=utf8')
        self.shema = 'data_play'

    def run(self):
        print('\033 [95m 开始写入：{} \033[0m'.format(self.threadname))
        self.dump_orders_log_by_hour()

    def dump_orders_log_by_date(self):
        '''
        172.16.240.77 -> BigData_CRM -> OrdersLog
        '''
        #找出总共多少天数
        sql1 = 'select TOP 1000 CONVERT(varchar(12), OperatorTime, 111) dt \
                from OrdersLog group by CONVERT(varchar(12), OperatorTime, 111);'
        df1 = pd.read_sql(sql1, CONN_77)
        print("\033 [95m {}, 日期共：{} \033[0m".format(self.threadname, len(df1)))
        count = 0
        for date in df1.values:
            sql3 = " WITH max_t (name, m_time) AS \
                    (SELECT  OrdersCode, MAX(OperatorTime) \
                    FROM  OrdersLog \
                    WHERE CONVERT(varchar(12), OperatorTime, 111 )='{date}' \
                    GROUP BY OrdersCode) \
                    SELECT DISTINCT OrdersCode, OrderStatus, OperatorTime \
                    FROM OrdersLog, max_t \
                    WHERE OrdersLog.OrdersCode = max_t.name AND OrdersLog.OperatorTime = max_t.m_time;".format(date=date.tolist()[0])
            df3 = pd.read_sql(sql3, CONN_77)
            count += 1
            #dataframe = df2.iloc[df2.groupby('orderscode').apply(lambda t: t['OperatorTime'].idxmax())]
            try:
                #import pdb
                #pdb.set_trace()
                pd.io.sql.to_sql(df3,'shw_opr_sls_total_day', self.connect, schema=self.shema, if_exists='append', index=False)
                print("\033 [96m {}, 已保存{}个，保存日期：{} , 共 {} 条记录\033[0m".format(self.threadname, count, date, len(df2)))
            except exc.IntegrityError as e:
                #print('\033[96m error:{} \033[0m'.format(e))
                continue

    def dump_orders_log_by_hour(self):
        '''
        先取 2017年
        '''
        sql1 = "SELECT DISTINCT CONVERT(varchar(12), OperatorTime, 111 ) \
                FROM OrdersLog WHERE DATEPART(yy, OperatorTime) = '2017';"
        df1 = pd.read_sql(sql1, CONN_77)
        print("\033 [95m {}, 日期共：{} \033[0m".format(self.threadname, len(df1)))
        count = 0
        for date in df1.values:
            sql2 = "with max_t (name, m_time) as \
                    (select  OrdersCode, max(OperatorTime)  \
                    from OrdersLog \
                    where CONVERT(varchar(12), OperatorTime, 111 )='{date}' \
                    group by OrdersCode, DATEPART(hh, OperatorTime)) \
                    select distinct OrdersCode, OrderStatus, OperatorTime \
                    from OrdersLog, max_t \
                    where OrdersLog.OrdersCode = max_t.name and OrdersLog.OperatorTime = max_t.m_time;".format(date=date.tolist()[0])
            df2 = pd.read_sql(sql2, CONN_77)
            count += 1
            try:
                pd.io.sql.to_sql(df2,'shw_opr_sls_total_hour', self.connect, schema=self.shema, if_exists='append', index=False)
                print("\033 [96m {}, 已保存{}个，保存日期：{} , 共 {} 条记录\033[0m".format(self.threadname, count, date, len(df2)))
            except exc.IntegrityError as e:
                #print('\033[96m error:{} \033[0m'.format(e))
                continue


if __name__ == '__main__':
    hour_thread = DataApi('Hour-Thread')
    day_thread = DataApi('Hour-Thread')
    hour_thread.start()
    day_thread.start()




