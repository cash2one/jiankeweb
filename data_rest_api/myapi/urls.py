from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from myapi import views

urlpatterns = [
    #url(r'^', include(router.urls)),
    url(r'^products/$', views.ApiTestList.as_view()),
    url(r'^products/(?P<pk>[0-9]+)/$', views.ApiTestDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
