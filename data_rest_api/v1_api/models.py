#coding:utf-8

import logging

from django.db import models

logger = logging.getLogger('data')

class DailyOrders(models.Model):
    '''
    每天实际销售情况表（订单记录锁死）
    '''
    day = models.DateField(verbose_name='日期')
    sls = models.DecimalField(verbose_name='销售金额(元)', max_digits=50, decimal_places=5)
    returned = models.DecimalField(verbose_name='退货金额(元)', max_digits=50, decimal_places=5)
    rejected = models.DecimalField(verbose_name='拒收金额(元)', max_digits=50, decimal_places=5)
    canceled = models.DecimalField(verbose_name='取消金额(元)', max_digits=50, decimal_places=5)

    class Meta:
        db_table = 'shw_opr_odrs_sts_day'


class HourlyGMV(models.Model):
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


class MonthlyRegionUser(models.Model):
    '''
    每月的地域新老用户比例
    '''
    year = models.IntegerField(verbose_name='年份', null=True)
    month = models.IntegerField(verbose_name='月份', null=True)
    region_code = models.CharField(verbose_name='地域编号', max_length=10, null=True)
    user_type = models.CharField(verbose_name='新老用户', max_length=10, null=True)
    user_cnt = models.IntegerField(verbose_name='客户数', null=True)

    class Meta:
        db_table = 'shw_opr_region_user_month'


class TmallIndustryTrend(models.Model):
    '''
    天猫品类（三级）交易情况，趋势
    '''
    year = models.IntegerField(verbose_name='年份', null=True)
    week = models.IntegerField(verbose_name='周', null=True)
    fst_cate = models.CharField(verbose_name='品类(一级目录)', max_length=255, null=True)
    scd_cate = models.CharField(verbose_name='品类(二级目录)', max_length=255, null=True)
    thd_cate = models.CharField(verbose_name='品类(三级目录)', max_length=255, null=True)
    trade_index = models.DecimalField(verbose_name='交易指数合计',
                                      max_digits=20, decimal_places=2, null=True)
    pay_item_qty = models.BigIntegerField(verbose_name='付款数量合计')
    item_cnt = models.BigIntegerField(verbose_name='类下获取到的商品数量')
    avg_trd_idx = models.DecimalField(verbose_name='（品类下）商品的平均交易指数',
                                      max_digits=20, decimal_places=2, null=True)
    avg_pay_qty = models.DecimalField(verbose_name='（品类下）商品的平均付款数量',
                                      max_digits=20, decimal_places=2, null=True)

    class Meta:
        db_table = 'shw_prc_sycm_trd_idx'


