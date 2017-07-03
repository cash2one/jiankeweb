# -*- coding:utf-8 -*-

import pandas as pd
import MySQLdb
import plotly.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go

CONN = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='jianke@123',
        db='big_data_platform',
        port=3306,
        charset='utf8'
      )

class SeriesCharts(object):

    def __init__(self):
        self.db_conn = CONN

    def line_charts(self):
        '''
        折线图
        '''
        sql = 'select collect_time, sum(old_sale_num_30) sum_old, sum(IFNULL(old_sale_num_30,0) + IFNULL(sale_num_growth,0)) sum_new  from shw_tmall_baojian_week group by collect_time;'
        df = pd.read_sql(sql, self.db_conn)
        trace_old = go.Scatter(
                x=df['collect_time'],
                y=df['sum_old'],
                name='上月',
                line = dict(color = '#17BECF'),
                opacity = 0.8)
        trace_new = go.Scatter(
                x=df['collect_time'],
                y=df['sum_new'],
                name='本月',
                line = dict(color = '#FF77FF'),
                opacity = 0.8)

        data = [trace_old, trace_new]
        layout = dict(
                height = 280,
                #title = "Manually Set Date Range",
                yaxis = dict(
                    range = [0,300000]),
                xaxis = dict(
                    range = ['2017-07-03','2016-11-21']),
                margin = dict(
                    l=65,
                    r=50,
                    b=55,
                    t=30
                    )
                )
        fig = dict(data=data, layout=layout)
        #import pdb
        #pdb.set_trace()
        #plot_div = py.iplot(fig, filename = "Manually Set Range")
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
