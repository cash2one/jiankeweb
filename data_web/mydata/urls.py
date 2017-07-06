from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

#from django.contrib.auth import views as auth_views

from mydata.views import IndexView,\
        LoginView,logout,\
        TablesView, TablesDynamicView

urlpatterns = [
    url(r'login/?$', LoginView.as_view(), name='login'),
    #url(r'^login/$', auth_views.login, {'template_name': 'mydata/login.html'}, name='login'),
    url(r'logout/?$', logout, name='logout'),
    url(r'index/?$', login_required(IndexView.as_view(), login_url='/mydata/dashboard/login'), name='index'),
    url(r'tables/?$', login_required(TablesView.as_view(), login_url='/mydata/dashboard/login'), name='tables'),
    url(r'dynamic/?$', TablesDynamicView.as_view(), name='tables_dynamic'),
    #url(r'dashboard/temp/?$', TempPlotView.as_view(), name='temp'),
]
