#coding:utf-8

import logging

from django.db import models

logger = logging.getLogger('data')

class OrdersLog(models.Model):
    OrdersCode = models.CharField(verbose_name='订单码', max_length=50)
    OrderStatus = models.IntegerField(verbose_name='订单状态')
    OperatorTime = models.DateTimeField(verbose_name='当天最后操作时间')

    class Meta:
        db_table = 'shw_opr_sls_total_day'


class HourGMV(models.Model):
    '''
    GMV流水(每分钟更新)
    '''
    day = models.DateField(verbose_name='日期')
    hour = models.IntegerField(verbose_name='小时')
    gmv = models.DecimalField(verbose_name='订单流水', max_digits=50, decimal_places=5)
    ords_cnt = models.BigIntegerField(verbose_name='订单数')
    user_cnt = models.BigIntegerField(verbose_name='客户数')

    class Meta:
        db_table = 'shw_opr_ords_gmv_hour'


class NewestTmall(models.Model):
    '''
    天猫最新价格
    '''
    taobao_id = models.IntegerField(verbose_name='淘宝ID', null=True)
    jk_id = models.IntegerField(verbose_name='健客ID', null=True)
    prod_name = models.CharField(verbose_name='搜索关键词', max_length=100, null=True)
    shop_name = models.CharField(verbose_name='天猫商铺名', max_length=100, null=True)
    price = models.DecimalField(verbose_name='天猫售价', max_digits=10, decimal_places=2, null=True)
    purchase_price = models.DecimalField(verbose_name='成本价', max_digits=10, decimal_places=2, null=True)
    margin = models.DecimalField(verbose_name='毛利率', max_digits=10, decimal_places=2, null=True)
    insert_time = models.DateTimeField(verbose_name='更新时间', null=True)

    class Meta:
        db_table = 'shw_prc_tmall_last'


