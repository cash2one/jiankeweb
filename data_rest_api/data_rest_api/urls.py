#coding:utf-8

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

import v1_api.views

router = DefaultRouter()
router.register(r'v1', v1_api.views.DailyOrdersViewSet)
router.register(r'v1', v1_api.views.HourlyGMVViewSet)
router.register(r'v1', v1_api.views.NewestTmallViewSet)
router.register(r'v1', v1_api.views.MonthlyRegionUserViewSet)
router.register(r'v1', v1_api.views.TmallIndustryTrendViewSet)
router.register(r'v1', v1_api.views.MonthlyImportedDurgSalesViewSet)
router.register(r'v1', v1_api.views.DailyTopHundredGMVViewSet)
router.register(r'v1', v1_api.views.DailyOrdersOriginGMVViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^', include(router.urls)),
#    url(r'^', include('myapi.urls', namespace='myapi')),
]


