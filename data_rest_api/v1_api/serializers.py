from django.shortcuts import render

from rest_framework import serializers

from v1_api.models import DailyOrders, HourlyGMV, NewestTmall,\
    MonthlyRegionUser, TmallIndustryTrend, MonthlyImportedDurgSales,\
    DailyTopHundredGMV, DailyOrdersOriginGMV

class DailyOrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyOrders
        fields = ('id', 'day', 'sls', 'returned',
                  'rejected', 'canceled')


class HourlyGMVSerializer(serializers.ModelSerializer):

    class Meta:
        model = HourlyGMV
        fields = ('id', 'day', 'hour', 'gmv', 'ords_cnt', 'user_cnt')


class NewestTmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewestTmall
        fields = ('id', 'taobao_id', 'jk_id', 'prod_name',
                  'shop_name', 'price', 'purchase_price',
                  'margin', 'insert_time')


class MonthlyRegionUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthlyRegionUser
        fields = ('id', 'year', 'month', 'region_code',
                  'user_type', 'user_cnt')


class   TmallIndustryTrendSerializer(serializers.ModelSerializer):

    class Meta:
        model = TmallIndustryTrend
        fields = ('id', 'year', 'week', 'fst_cate',
                  'scd_cate', 'thd_cate', 'trade_index',
                  'pay_item_qty', 'item_cnt', 'avg_trd_idx',
                  'avg_pay_qty')


class MonthlyImportedDurgSalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthlyImportedDurgSales
        fields = ('id', 'year', 'month', 'sls_impt',
                  'qty_impt', 'sls_ttl', 'qty_ttl',
                  'impr_per')


class DailyTopHundredGMVSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyTopHundredGMV
        fields = ('id', 'day', 'product_code',
                  'gmv', 'qty', 'rank')


class DailyOrdersOriginGMVSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyOrdersOriginGMV
        fields = ('id', 'day', 'origin_type', 'ords_cnt',
                  'gmv', 'user_cnt')

