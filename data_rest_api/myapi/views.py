#coding:utf-8

import logging

#from django.http import HttpResponse, JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser
#from django.http import Http404
#from rest_framework.views import APIView
from rest_framework import status
#from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from myapi.models import ApiTest
from myapi.serializers import ApiTestSerializer, UserSerializer

logger = logging.getLogger('data_request')

#@csrf_exempt
#def taobao_list(request):
#    """
#    List all code snippets, or create a new snippet.
#    """
#    if request.method == 'GET':
#        items = ApiTest.objects.filter(id__lt=10)
#        serializer = ApiTestSerializer(items, many=True)
#        return JsonResponse(serializer.data, safe=False)
#
#    elif request.method == 'POST':
#        data = JSONParser().parse(request)
#        serializer = ApiTestSerializer(data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=201)
#        return JsonResponse(serializer.errors, status=400)

#@api_view(['GET', 'POST'])
#def taobao_list(request, format=None):
#    """
#    List all snippets, or create a new snippet.
#    """
#    if request.method == 'GET':
#        items = ApiTest.objects.filter(id__lt=10)
#        serializer = ApiTestSerializer(items, many=True)
#        return Response(serializer.data)
#
#    elif request.method == 'POST':
#        logger.debug('\033[96m POST:{} \033[0m'.format(request.data))
#        serializer = ApiTestSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@csrf_exempt
#def taobao_detail(request, pk):
#    """
#    Retrieve, update or delete a code taobao.
#    """
#    try:
#        item = ApiTest.objects.get(pk=pk)
#    except ApiTest.DoesNotExist:
#        return HttpResponse(status=404)
#
#    if request.method == 'GET':
#        serializer = ApiTestSerializer(item)
#        return JsonResponse(serializer.data)
#
#
#    elif request.method == 'PATCH':
#        data = JSONParser().parse(request)
#        logger.debug('\033[96m patch data: {} \033[0m'.format(data))
#        serializer = ApiTestSerializer(item, data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return JsonResponse(serializer.errors, status=400)
#
#    elif request.method == 'PUT':
#        data = JSONParser().parse(request)
#        logger.debug('\033[96m put data: {} \033[0m'.format(data))
#        serializer = ApiTestSerializer(item, data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return JsonResponse(serializer.errors, status=400)
#
#    elif request.method == 'DELETE':
#        item.delete()
#        return HttpResponse(status=204)

#class ApiTestList(APIView):
#    """
#    List all snippets, or create a new snippet.
#    """
#    def get(self, request, format=None):
#        snippets = ApiTest.objects.filter(id__lt=10)
#        serializer = ApiTestSerializer(snippets, many=True)
#        return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = ApiTestSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import permissions

class ApiTestList(generics.ListCreateAPIView):
    queryset = ApiTest.objects.filter(id__lt=10)
    serializer_class = ApiTestSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        #import pdb
        #pdb.set_trace()
        serializer.save(owner=self.request.user)

#@api_view(['GET', 'PUT', 'DELETE'])
#def taobao_detail(request, pk, format=None):
#    """
#    Retrieve, update or delete a snippet instance.
#    """
#    try:
#        snippet = ApiTest.objects.get(pk=pk)
#    except ApiTest.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)
#
#    if request.method == 'GET':
#        serializer = ApiTestSerializer(snippet)
#        return Response(serializer.data)
#
#    elif request.method == 'PUT':
#        serializer = ApiTestSerializer(snippet, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    elif request.method == 'DELETE':
#        snippet.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

#class ApiTestDetail(APIView):
#    """
#    Retrieve, update or delete a snippet instance.
#    """
#    def get_object(self, pk):
#        try:
#            return ApiTest.objects.get(pk=pk)
#        except ApiTest.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = ApiTestSerializer(snippet)
#        return Response(serializer.data)
#
#    def put(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = ApiTestSerializer(snippet, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        snippet.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

class ApiTestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApiTest.objects.all()
    serializer_class = ApiTestSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = ApiTest.objects.all()
    serializer_class = ApiTestSerializer

    def _display_product(self, product=None):
        if product :
            data = ApiTest.objects.filter(prod_name=product)
        else:
            data = ApiTest.objects.all()[:10]
        return data

    @list_route(methods=['get'], url_path='display/product')
    def display_product(self, request):
        product = request.query_params.get('product')
        if product:
            logger.debug('\033[95m product:{} \033[0m'.format(product))
            products = self._display_product(product)
            context = {
                'status': status.HTTP_200_OK,
                'msg': 'OK',
                'data': ApiTestSerializer(products, many=True).data,
            }
        else:
            products = self._display_product()
            context = {
                'status': status.HTTP_200_OK,
                'msg': 'OK',
                'data': ApiTestSerializer(products, many=True).data,
            }
        return Response(context, status=context.get('status'))


    @list_route(methods=['get'], url_path='search/product')
    def search_product(self, request):
        product = request.query_params.get('product')
        if product:
            logger.debug('\033[95m product:{} \033[0m'.format(product))
            products = ApiTest.objects.filter(prod_name__icontains=product).distinct()
            context = {
                'status': status.HTTP_200_OK,
                'msg': 'OK',
                'data': products.values('prod_name'),
            }
        else:
            context = {
                'status': status.HTTP_400_BAD_REQUEST,
                'msg': '请提供搜索条件!',
            }
        return Response(context, status=context.get('status'))

