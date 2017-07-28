from django.shortcuts import render

from rest_framework import serializers

from v1_api.models import DailyOrders, HourlyGMV, NewestTmall

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


