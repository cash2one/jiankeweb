#coding:utf-8

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

import v1_api.views

router = DefaultRouter()
router.register(r'v1', v1_api.views.OrdersLogViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
#    url(r'^', include('myapi.urls', namespace='myapi')),
]


urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]