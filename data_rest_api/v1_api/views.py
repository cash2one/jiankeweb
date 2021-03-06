#coding:utf-8

import logging
import datetime
import pprint

from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from v1_api.models import OrdersLog, HourGMV, NewestTmall
from v1_api.serializers import OrdersLogSerializer,\
			OrdersLogRetrieveSerializer, HourGMVSerializer,\
            NewestTmallSerializer

logger = logging.getLogger('data_request')

def _show_client_info(request):
    client_info = { key.lower():request.META.get(key)
        for key in ['REMOTE_ADDR', 'REMOTE_HOST', 'REMOTE_USER', 'REQUEST_METHOD']}
    client_info['is_ajax'] = request.is_ajax()
    return client_info

def _show_response_headers(response):
    response_headers = response.items()
    return response_headers


class OrdersLogViewSet(viewsets.ModelViewSet):
    queryset = OrdersLog.objects.all()
    serializer_class = OrdersLogSerializer

    def _filter_log_date(self, items, since, until):
        date_list = items.extra({'operate_time':"date(OperatorTime)"}) \
            .values('operate_time').distinct()
        if all([since, until]):
            if since > until:
                return 'error'
            #import pdb
            #pdb.set_trace()
            date_list = date_list.filter(OperatorTime__gte=since, OperatorTime__lte=until)
        return date_list

    @list_route(methods=['get'], url_path='orders/day')
    def get_orders_log_per_day(self, request, format=None):
        '''
        订单日志接口
        '''
        #items = OrdersLog.objects.all()
        #import pdb
        #pdb.set_trace()
        logger.debug('\033[95m request client info : {} \033[0m'.format(_show_client_info(request)))
        items = self.queryset.filter(id__lt=592351)
        since = request.query_params.get('since')
        until = request.query_params.get('until')
        logger.debug('\033[96m query params:since:{}, until:{} \033[0m'\
                     .format(since, until))
        date_list = self._filter_log_date(items, since, until)
        if date_list == 'error':
            context = {
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'msg': 'NOT ACCEPTABLE',
                'data': '参数错误',
            }
            return Response(context, status=context.get('status'))
        data = []
        for date in date_list:
            date = date['operate_time']
            date_items = items \
                .filter(OperatorTime__startswith=date)
            sls_items = date_items.exclude(OrderStatus__in=[0, 100, 60, 80, 160, 170, 180, 200, 303])
            rejected_items = date_items.filter(OrderStatus__in=[60, 160])
            returned_items = date_items.filter(OrderStatus__in=[80, 180])
            unconfirmed_items = date_items.filter(OrderStatus__in=[0, 100])
            data.append({
                'date': date,
                'GMV': '',
                'sls': len(sls_items),
                'returned': len(returned_items),
                'rejected': len(rejected_items),
                'unconfirmed': len(unconfirmed_items),
            })
        logger.debug('\033[96m orders log counts:{} \033[0m'.format(len(data)))
        context = {
            'status': status.HTTP_200_OK,
            'msg': 'OK',
            'data': data,
        }
        response = Response(context, status=context.get('status'))
        logger.debug('\033[95m response headers : {} \033[0m'.format(_show_response_headers(response)))
        return response


class HourGMVViewSet(viewsets.ModelViewSet):
    queryset = HourGMV.objects.all()
    serializer_class = HourGMVSerializer

    def _filter_gmv_hourly_query_params(self, queryset,
                                        since=None, until=None,
                                        last_date=None, next_date=None):
        if all([since, until]):
            if since > until:
                return
            data = queryset \
                .filter(day__lte=until, day__gte=since)\
                .values('hour')\
                .annotate(gmv=Sum('gmv'),
                          user_cnt=Sum('user_cnt'),
                          ords_cnt=Sum('ords_cnt'))
        elif all([last_date, next_date]):
            data = queryset.filter(day__in=[last_date, next_date])
            data = HourGMVSerializer(data, many=True).data
        else:
            data = queryset.filter(day=datetime.date.today())
            data = HourGMVSerializer(data, many=True).data
        return data

    @list_route(methods=['get'], url_path='gmv/hourly')
    def get_gmv_hourly(self, request, format=None):
        '''
        GMV流水(每小时)
        目前接口对接三种情况：
        1 不传参时，显示 今天 的数据；
        2 传参:last_date, next_date ，显示 特定某两天的数据;
        3 传参: since, until, 显示 某一段时间内加总的数据
        '''
        logger.debug('\033[95m request client info : {} \033[0m'.format(_show_client_info(request)))
        query_params = { key: request.query_params.get(key)
                        for key in ['since', 'until', 'last_date', 'next_date'] }
        logger.debug(pprint.pformat(query_params))
        data = self._filter_gmv_hourly_query_params(
            self.queryset, since=query_params['since'], until=query_params['until'],
            last_date=query_params['last_date'], next_date=query_params['next_date']
        )
        if not data:
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



