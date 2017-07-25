#coding:utf-8

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from v1_api.models import OrdersLog
from v1_api.serializers import OrdersLogSerializer,\
			OrdersLogRetrieveSerializer

logger = logging.getLogger('data_request')

class OrdersLogViewSet(viewsets.ModelViewSet):
    queryset = OrdersLog.objects.all()
    serializer_class = OrdersLogSerializer

    def _filter_log_date(self, items, since, util):
        date_list = items.extra({'operate_time':"date(OperatorTime)"}) \
            .values('operate_time').distinct()
        if any([since, util]):
            #import pdb
            #pdb.set_trace()
            date_list = date_list.filter(OperatorTime__gte=since, OperatorTime__lt=util)
        return date_list

    @list_route(methods=['get'], url_path='orders/day')
    def get_orders_log_per_day(self, request):
        '''
        订单日志接口
        '''
        items = OrdersLog.objects.all()
        #import pdb
        #pdb.set_trace()
        #items = OrdersLog.objects.filter(id__lt=3592351)
        since = request.query_params.get('since')
        util = request.query_params.get('util')
        logger.debug('\033[96m query params:since:{}, util:{} \033[0m'\
                     .format(since, util))
        date_list = self._filter_log_date(items, since, util)
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
        return Response(context, status=context.get('status'))

