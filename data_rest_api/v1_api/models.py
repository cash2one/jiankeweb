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


