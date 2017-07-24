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


