# -*- coding:utf-8 -*-

import os

import pandas as pd
import MySQLdb
import plotly.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go
from plotly import tools

from data_web.settings import DB_6_HOST,\
        DB_6_USER, DB_6_PASSWD, DB_6_PORT,\
        DB_6, DB_HOST, DB_USER, DB_PASSWD, DB_PORT

CONN_6 = MySQLdb.connect(
        host=DB_6_HOST,
        user=DB_6_USER,
        passwd=DB_6_PASSWD,
        db=DB_6,
        port=DB_6_PORT,
        charset='utf8'
      )

CONN = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWD,
        db='big_data_platform',
        port=DB_PORT,
        charset='utf8'
      )


class SeriesCharts(object):

    def __init__(self):
        self.db_conn = CONN

    def line_chart(self):
        '''
        折线图
        '''
        sql = 'select collect_time, \
                sum(old_sale_num_30) sum_old, \
                sum(IFNULL(old_sale_num_30,0) + IFNULL(sale_num_growth,0)) sum_new \
                from shw_tmall_baojian_week group by collect_time;'
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
                width = 340,
                #title = "Manually Set Date Range",
                yaxis = dict(
                    autorange=False,
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    autotick=True,
                    ticks='',
                    showticklabels=False,
                    range = [0,300000],
                    ),
                xaxis = dict(
                    tickfont=dict(
                        size=10,
                        color='rgb(107, 107, 107)'
                    ),
                    range = ['2017-07-03','2016-11-21']),
                margin = dict(
                    l=45,
                    r=75,
                    b=55,
                    t=30
                    )
                )
        fig = dict(data=data, layout=layout)
        #import pdb
        #pdb.set_trace()
        #plot_div = plot(fig, output_type='div', include_plotlyjs=False, show_link=False)
        HTMLlink = plot(fig, show_link=False, auto_open=False)[7:]
        with open(HTMLlink, 'r') as plot_file :
            tempHTML = plot_file.read()
        os.remove(HTMLlink)
        tempHTML = tempHTML.replace('displaylogo:!0', 'displaylogo:!1')
        tempHTML = tempHTML.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud"]')
        return tempHTML

    def bar_chart(self):
        '''
        条形图
        '''
        sql = 'select sum(old_price) sum_old, \
                sum(price) sum_new, \
                jk_prod_name from shw_comweb_price_all group by jk_prod_name limit 5;'
        df = pd.read_sql(sql, self.db_conn)
        trace_old = go.Bar(
            x=df['jk_prod_name'],
            y=df['sum_old'],
            name='原价',
            marker=dict(
                color='rgb(55, 83, 109)'
            )
        )
        trace_new = go.Bar(
            x=df['jk_prod_name'],
            y=df['sum_new'],
            name='新价',
            marker=dict(
                color='rgb(26, 118, 255)'
            )
        )
        data = [trace_old, trace_new]
        layout = go.Layout(
            #title='US Export of Plastic Scrap',
            xaxis=dict(
                tickfont=dict(
                    size=6,
                    color='rgb(107, 107, 107)'
                )
            ),
            yaxis=dict(
                #title='Price (RMB)',
                titlefont=dict(
                    size=16,
                    color='rgb(107, 107, 107)'
                ),
                tickfont=dict(
                    size=14,
                    color='rgb(107, 107, 107)'
                )
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            margin = dict(
                l=35,
                r=25,
                b=55,
                t=30
                ),
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1
        )
        
        fig = go.Figure(data=data, layout=layout)
        #py.iplot(fig, filename='style-bar')
        plot_div = plot(fig, output_type='div', include_plotlyjs=False, show_link=False)
        return plot_div

    def pie_chart(self):
        '''
        饼图
        '''
        sql = 'select sum(float_home) s0, \
                sum(float_prod) s1, sum(from_prod) s2, \
                sum(wechat_mall) s3, sum(from_engine) s4, \
                sum(from_other) s5, sum(imm_down) s6 \
                from shw_mo_mall_down ;'
        df = pd.read_sql(sql, self.db_conn)
        labels =  [
                "FloatHome",
                "FloatProd",
                "FromProd",
                "WechatMall",
                "FromEngine",
                "FromOther",
                "ImmDown"
              ]
        values = [df.s0[0], df.s1[0], df.s2[0], df.s3[0], df.s4[0], df.s5[0], df.s6[0]]
        colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1', '#FF95CA', '#4EFEB3', '#46A3FF']
        
        trace = go.Pie(labels=labels, values=values,
                       hoverinfo='label+percent', textinfo='value', 
                       textfont=dict(size=10),
                       marker=dict(colors=colors, 
                                   line=dict(color='#FFFFFF', width=2)))
        layout = go.Layout(height = 280,
                           width = 750,
                           autosize = False,
                           margin = dict(
                               l=85,
                               r=35,
                               b=35,
                               t=15
                               ),
                           #title = 'Main title'
                           )
        fig = go.Figure(data = [trace], layout = layout) 
        #py.iplot([trace], filename='styled_pie_chart')
        plot_div = plot(fig, output_type='div', include_plotlyjs=False, show_link=False)
        #plot_div = plot([trace], show_link=False, auto_open=False)[7:]
        return plot_div

    def decimal_to_percent(self, decimal):
        return "%.2f%%" % (decimal*100)
    
    def test_bar_chart(self):
        sql = "select shop_name, price, purchase_price \
                from  scrapy_taobao_cfy \
                where prod_name='龙心 芪龙胶囊 0.2g*12粒/盒'\
                and batch_id=2017070710  order by price desc ;"

        df = pd.read_sql(sql, CONN_6)
        #import pdb
        #pdb.set_trace()
        shop_list = df.shop_name.values.tolist()
        price_list = df.price.values.tolist()
        max_price = int(max(price_list))
        min_price = int(min(price_list))
        tickvals = list(range(min_price+5, max_price+5, 5))
        purchase_price = df.purchase_price.values[0]
        profits = [ self.decimal_to_percent((x-purchase_price)/purchase_price)
                for x in price_list ]
        trace1 = go.Bar(
                x = shop_list,
                y = price_list,
                name='最新售价',
                #width = [0.4],  #Customizing Individual Bar Widths
                marker = dict(
                    line=dict(
                        width=0.5, # 条形的边框粗细程度
                        ),
                    color=[
                         'rgba(50, 171, 96, 0.6)', 'rgba(50, 171, 96, 0.6)',
                         'rgba(50, 171, 96, 0.6)', 'rgba(50, 171, 96, 0.6)',
                         'rgba(222,45,38,0.8)', 'rgba(50, 171, 96, 0.6)', 
                         'rgba(50, 171, 96, 0.6)','rgba(50, 171, 96, 0.6)', 
                         'rgba(50, 171, 96, 0.6)', 'rgba(50, 171, 96, 0.6)',
                         'rgba(50, 171, 96, 0.6)']),
                     )
        trace2 = go.Scatter(
                x = shop_list,
                y = profits,
                xaxis='x2',
                yaxis='y2',
                name='毛利率',
                marker=dict(color='rgb(148, 103, 189)'),
                )

        data = [trace1, trace2]
        #data = [trace0]
        layout = go.Layout(
                title='龙心 芪龙胶囊 0.2g*12粒/盒',
                height = 480,
                legend=dict(
                    orientation="h",
                    x=-.1, y=1.2
                    ),
                yaxis=dict(
                    title='价格',
                    tickvals = [5,10,15,20,25,30,35,40,45,50,55,60],
                    #tickvals = tickvals,
                    tickwidth=2,
                    ticksuffix='元',
                    showtickprefix='first',
                    ),
                xaxis2=dict(
                    showgrid=False,
                    showticklabels=False,
                    #linecolor='#000',
                    overlaying='x',
                    ),
                yaxis2=dict(
                    title='毛利率',
                    zeroline=False,
                    tickfont=dict(
                        color='rgb(148, 103, 189)'
                        ),
                    titlefont=dict(
                        color='rgb(148, 103, 189)'
                        ),
                    nticks=9,
                    overlaying='y',
                    side='right',
                    #tickvals = ['{}%'.format(x) for x in range(-300, 100, 50)],
                    range = ['-300', '100'],
                    ticksuffix = '%',
                    #text=str(300) + '%',
                    ),
                )
        fig = go.Figure(data=data, layout=layout)

        #py.iplot(fig, filename='style-bar')
        plot_div = plot(fig, output_type='div', include_plotlyjs=False, show_link=False)
        return plot_div

    def test2_bar_chart(self):
        sql = "select shop_name, price, purchase_price \
                from  scrapy_taobao_cfy \
                where prod_name='龙心 芪龙胶囊 0.2g*12粒/盒' and batch_id=2017070710;"

        df = pd.read_sql(sql, CONN_6)
        #import pdb
        #pdb.set_trace()
        shop_list = df.shop_name.values.tolist()
        price_list = df.price.values.tolist()
        purchase_price = df.purchase_price.values[0]
        profits = [ self.decimal_to_percent((x-purchase_price)/purchase_price)
                for x in price_list ]
        trace0 = go.Bar(
                x = shop_list,
                y = price_list,
                name='最新售价',
                marker = dict(
                    line=dict(
                        width=0.5, # 条形的边粗程度
                        ),
                    color=[
                         'rgba(50, 171, 96, 0.6)', 'rgba(50, 171, 96, 0.6)',
                         'rgba(50, 171, 96, 0.6)', 'rgba(50, 171, 96, 0.6)',
                         'rgba(50, 171, 96, 0.6)', 'rgba(50, 171, 96, 0.6)',
                         'rgba(50, 171, 96, 0.6)', 'rgba(222,45,38,0.8)',
                         'rgba(50, 171, 96, 0.6)', 'rgba(50, 171, 96, 0.6)',
                         'rgba(50, 171, 96, 0.6)']),
                     )
        trace1 = go.Scatter(
                x = shop_list,
                y = profits,
                yaxis='y2',
                name='毛利率',
                #marker=dict(color='rgb(148, 103, 189)'),
                mode='lines+markers',
                line=dict(
                    color='rgb(128, 0, 128)'),
                )

        data = [trace0, trace1]
        #data = [trace0]
        layout = dict(
                title='龙心 芪龙胶囊 0.2g*12粒/盒',
                height = 480,
                xaxis=dict(
                    showgrid=False,
                    showline=False,
                    showticklabels=True,
                    domain=[0, 0.85],
                    ),
                xaxis2=dict(
                    showgrid=False,
                    #showline=True,
                    showticklabels=False,
                    #linecolor='rgba(102, 102, 102, 0.8)',
                    #linewidth=2,
                    domain=[0, 0.85],
                    ),
                yaxis=dict(
                    title='价格',
                    tickvals = [5,10,15,20,25,30,35,40,45,50,55,60],
                    tickwidth=2,
                    ),
                yaxis2=dict(
                    title='毛利率',
                    tickfont=dict(
                        color='rgb(148, 103, 189)'
                        ),
                    titlefont=dict(
                        color='rgb(148, 103, 189)'
                        ),
                    overlaying='y',
                    side='right',
                    range = ['-320', '100'],
                    ),
                paper_bgcolor='rgb(248, 248, 255)',
                plot_bgcolor='rgb(248, 248, 255)',
                )
        fig = tools.make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=False, vertical_spacing=0.001)
        fig.append_trace(trace0, 1, 1)
        fig.append_trace(trace1, 1, 2)
        fig['layout'].update(layout)

        #fig = go.Figure(data=data, layout=layout)

        #py.iplot(fig, filename='style-bar')
        plot_div = plot(fig, output_type='div', include_plotlyjs=False, show_link=False)
        return plot_div








