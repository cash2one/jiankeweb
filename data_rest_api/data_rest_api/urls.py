#coding:utf-8

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

import myapi.views

router = DefaultRouter()
router.register(r'snippets', myapi.views.ProductViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^', include('myapi.urls', namespace='myapi')),
]


urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
