from django.shortcuts import render

from rest_framework import serializers

from v1_api.models import OrdersLog, HourGMV, NewestTmall

class OrdersLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdersLog
        fields = ('id', 'OrdersCode', 'OrderStatus', 'OperatorTime')


class OrdersLogRetrieveSerializer(serializers.Serializer):
    date = serializers.DateTimeField(read_only=True)
    GMV = serializers.CharField(required=False)
    sls = serializers.IntegerField()
    returned = serializers.IntegerField()
    rejected = serializers.IntegerField()
    unconfirmed = serializers.IntegerField()


class HourGMVSerializer(serializers.ModelSerializer):

    class Meta:
        model = HourGMV
        fields = ('id', 'day', 'hour', 'gmv', 'ords_cnt', 'user_cnt')


class NewestTmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewestTmall
        fields = ('id', 'taobao_id', 'jk_id', 'prod_name',
                  'shop_name', 'price', 'purchase_price',
                  'margin', 'insert_time')


