#coding:utf-8

from django.contrib.auth.models import User
from rest_framework import serializers

from myapi.models import ApiTest

class UserSerializer(serializers.ModelSerializer):
    apitest = serializers.PrimaryKeyRelatedField(many=True, queryset=ApiTest.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'apitest')

class ApiTestSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = ApiTest
        fields =('id', 'jk_id', 'taobao_id', 'prod_name',
                 'prod_class', 'num', 'price', 'purchase_price',
                 'marigin', 'real_name', 'shop_name', 'price_rank', 'price_idx', 'owner',)
