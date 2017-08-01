#coding:utf-8

import logging
import time
import datetime
from collections import OrderedDict
import MySQLdb

from django.db.models import Sum
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from v1_api.models import *
from v1_api.serializers import *

from data_rest_api.settings import DB6_HOST, DB6_USER, DB6_PASSWD,\
    DB6, DB6_CHARSET

logger = logging.getLogger('data_request')

def _show_client_info(request):
    client_info = { key.lower():request.META.get(key)
        for key in ['REMOTE_ADDR', 'REMOTE_HOST', 'REMOTE_USER', 'REQUEST_METHOD']}
    client_info['is_ajax'] = request.is_ajax()
    return client_info

def _show_response_headers(response):
    response_headers = response.items()
    return response_headers


class DailyOrdersViewSet(viewsets.ModelViewSet):
    queryset = DailyOrders.objects.all()
    serializer_class = DailyOrdersSerializer

    def _filter_log_date(self, queryset, since, until):
        #date_list = queryset.extra({'operate_time':"date(OperatorTime)"}) \
        #    .values('operate_time').distinct()
        try:
            if all([since, until]):
                if since > until: return 'error'
                queryset = queryset.filter(day__gte=since, day__lte=until)
        except ValidationError as e:
            logger.error('\033[92m {} \033[0m'.format(e))
            return 'error'
        return queryset

    @list_route(methods=['get'], url_path='daily/orders/?')
    def get_daily_orders(self, request, format=None):
        '''
        订单日志接口
        可提供参数: since, until
        '''
        logger.debug('\033[95m request client info : {} \033[0m'.format(_show_client_info(request)))
        since = request.query_params.get('since')
        until = request.query_params.get('until')
        logger.debug('\033[96m query params:since:{}, until:{} \033[0m'\
                     .format(since, until))
        data = self._filter_log_date(self.queryset, since, until)
        if data == 'error':
            context = {
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'msg': 'NOT ACCEPTABLE',
                'data': '参数错误',
            }
            return Response(context, status=context.get('status'))
        data = self.serializer_class(data, many=True).data
        logger.debug('\033[96m orders log counts:{} \033[0m'.format(len(data)))
        context = {
            'status': status.HTTP_200_OK,
            'msg': 'OK',
            'data': data,
        }
        response = Response(context, status=context.get('status'))
        logger.debug('\033[95m response headers : {} \033[0m'.format(_show_response_headers(response)))
        return response


class HourlyGMVViewSet(viewsets.ModelViewSet):
    queryset = HourlyGMV.objects.all()
    serializer_class = HourlyGMVSerializer

    def _filter_gmv_hourly_query_params(self, query_params):
        query_values = query_params.values()
        since, until, last_date, next_date = query_values
        if all([since, until]):
            if since > until: return 'error'
            data = self.queryset \
                .filter(day__lte=until, day__gte=since)\
                .values('hour')\
                .annotate(gmv=Sum('gmv'),
                          user_cnt=Sum('user_cnt'),
                          ords_cnt=Sum('ords_cnt'))
        elif all([last_date, next_date]):
            data = self.queryset.filter(day__in=[last_date, next_date])
            data = self.serializer_class(data, many=True).data
        else:
            data = self.queryset.filter(day=datetime.date.today())
            data = self.serializer_class(data, many=True).data
        return data

    @list_route(methods=['get'], url_path='gmv/hourly')
    def get_hourly_gmv(self, request, format=None):
        '''
        GMV流水(每小时)
        目前接口对接三种情况：
        1 不传参时，显示 今天 的数据；
        2 传参:last_date, next_date ，显示 特定某两天的数据;
        3 传参: since, until, 显示 某一段时间内加总的数据
        '''
        logger.debug('\033[95m request client info : {} \033[0m'.format(_show_client_info(request)))
        query_params = OrderedDict()
        keys = ['since', 'until', 'last_date', 'next_date']
        for key in keys:
            query_params[key] = request.query_params.get(key)
        logger.debug('\033[96m query params:{} \033[0m'.format(query_params))
        data = self._filter_gmv_hourly_query_params(query_params)
        if data == 'error':
            context = {
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'msg': 'NOT ACCEPTABLE',
                'data': '参数错误',
            }
            return Response(context, status=context.get('status'))
        logger.debug('\033[96m gmv hourly counts:{} \033[0m'.format(len(data)))
        context = {
            'status': status.HTTP_200_OK,
            'msg': 'OK',
            'data': data,
        }
        response = Response(context, status=context.get('status'))
        logger.debug('\033[95m response headers : {} \033[0m'.format(_show_response_headers(response)))
        return response


class NewestTmallViewSet(viewsets.ModelViewSet):
    queryset = NewestTmall.objects.all()
    serializer_class = NewestTmallSerializer

    @list_route(methods=['get'], url_path='newest/tmall/price')
    def get_newest_tmall_price(self, request, format=None):
        '''
        天猫最新价格:
        要求必须带参数 product 查询
        '''
        logger.debug('\033[95m request client info : {} \033[0m'.format(_show_client_info(request)))
        product = request.query_params.get('product')
        if not product:
            context = {
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'msg': 'NOT ACCEPTABLE',
                'data': '参数错误',
            }
            return Response(context, status=context.get('status'))
        items = self.queryset.filter(prod_name__icontains=product)
        data = self.serializer_class(items, many=True).data
        logger.debug('\033[96m newest tmall counts:{} \033[0m'.format(len(data)))
        context = {
            'status': status.HTTP_200_OK,
            'msg': 'OK',
            'data': data,
        }
        response = Response(context, status=context.get('status'))
        logger.debug('\033[95m response headers : {} \033[0m'.format(_show_response_headers(response)))
        return response


class MonthlyRegionUserViewSet(viewsets.ModelViewSet):
    queryset = MonthlyRegionUser.objects.all()
    serializer_class = MonthlyRegionUserSerializer

    def _filter_monthly_region_user(self, queryset, since, until):
        #import pdb
        #pdb.set_trace()
        if not all([since, until]) or since > until: return 'error'
        year_month = lambda x:(int(x[0]), int(x[1]))
        since_year, since_month = year_month(since.split('-'))
        until_year, until_month = year_month(until.split('-'))
        logger.debug('\033[96m since:year:{}, month:{}; until: year:{}, month:{} \033[0m'\
                     .format(since_year, since_month, until_year, until_month))
        if since_year == until_year:
            queryset = queryset.filter(year=until_year,
                                       month__gte=min(since_month, until_month),
                                       month__lte=max(since_month, until_month))
        else:
            queryset = queryset.filter(year__gte=min(since_year, until_year),
                                       year__lte=max(since_year, until_year),
                                       month__gte=min(since_month, until_month),
                                       month__lte=max(since_month, until_month))
        return queryset

    @list_route(methods=['get'], url_path='monthly/region/user')
    def get_monthly_region_user(self, request, format=None):
        '''
        每月的地域新老用户比例
        必须提供查询参数: since, until
        '''
        logger.debug('\033[95m request client info : {} \033[0m'.format(_show_client_info(request)))
        since = request.query_params.get('since')
        until = request.query_params.get('until')
        logger.debug('\033[96m query params:since:{}, until:{} \033[0m'\
                     .format(since, until))
        data = self._filter_monthly_region_user(self.queryset, since, until)
        if data == 'error':
            context = {
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'msg': 'NOT ACCEPTABLE',
                'data': '参数错误',
            }
            return Response(context, status=context.get('status'))
        data = self.serializer_class(data, many=True).data
        logger.debug('\033[96m monthly region user counts:{} \033[0m'.format(len(data)))
        context = {
            'status': status.HTTP_200_OK,
            'msg': 'OK',
            'data': data,
        }
        response = Response(context, status=context.get('status'))
        logger.debug('\033[95m response headers : {} \033[0m'.format(_show_response_headers(response)))
        return response


class TmallIndustryTrendViewSet(viewsets.ModelViewSet):
    queryset = TmallIndustryTrend.objects.all()
    serializer_class = TmallIndustryTrendSerializer

    def _filter_tmall_industry_trend(self, third_category):
        year = int(time.strftime("%Y"))
        week = int(time.strftime("%W"))
        if third_category:
            db = MySQLdb.connect(host=DB6_HOST, user=DB6_USER,
                               passwd=DB6_PASSWD, db=DB6, charset=DB6_CHARSET)
            cursor = db.cursor()
            cursor.execute("select model_name, trade_index, pay_item_qty  \
                           from industrys where third_category_id=\
                           (select second_category_id from industry_third_category \
                           where third_cate_name='{third_category}')"
                           .format(third_category=third_category))
            items = cursor.fetchall()
            data = []
            for item in items:
                data.append({
                    'model_name': item[0],
                    'trade_index': item[1],
                    'pay_item_qty': item[2],
                })
        else:
            queryset = self.queryset.filter(year=year, week=week)
            data = self.serializer_class(queryset, many=True).data
        return data

    @list_route(methods=['get'], url_path='tmall/industry/trend/?')
    def get_tmall_industry_trend(self, request, format=None):
        '''
        天猫品类（三级）交易情况，趋势
        可选参数: third_category
        '''
        logger.debug('\033[95m request client info : {} \033[0m'.format(_show_client_info(request)))
        third_category= request.query_params.get('third_category')
        logger.debug('\033[96m query params: third_category:{} \033[0m'\
                     .format(third_category))
        data = self._filter_tmall_industry_trend(third_category)
        logger.debug('\033[96m newest tmall counts:{} \033[0m'.format(len(data)))
        context = {
            'status': status.HTTP_200_OK,
            'msg': 'OK',
            'data': data,
        }
        response = Response(context, status=context.get('status'))
        logger.debug('\033[95m response headers : {} \033[0m'.format(_show_response_headers(response)))
        return response


class MonthlyImportedDurgSalesViewSet(viewsets.ModelViewSet):
    queryset = MonthlyImportedDurgSales.objects.all()
    serializer_class = MonthlyImportedDurgSalesSerializer

    @list_route(methods=['get'], url_path='monthly/imported/durg/sales/?')
    def get_monthly_imported_drug_sales(self, request, format=None):
        '''
        每个月进口药的销售占比（剔除 待确认、拒签、退货、取消 订单）
        '''
        logger.debug('\033[95m request client info : {} \033[0m'.format(_show_client_info(request)))
        data = self.serializer_class(self.queryset, many=True).data
        logger.debug('\033[96m monthly imported durg sales counts:{} \033[0m'.format(len(data)))
        context = {
            'status': status.HTTP_200_OK,
            'msg': 'OK',
            'data': data,
        }
        response = Response(context, status=context.get('status'))
        logger.debug('\033[95m response headers : {} \033[0m'.format(_show_response_headers(response)))
        return response


