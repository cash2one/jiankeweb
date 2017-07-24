from django.shortcuts import render

from rest_framework import serializers

from v1_api.models import OrdersLog

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
