from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

#from django.contrib.auth import views as auth_views

from mydata import views

urlpatterns = [
    url(r'login/?$', views.LoginView.as_view(), name='login'),
    #url(r'^login/$', auth_views.login, {'template_name': 'mydata/login.html'}, name='login'),
    url(r'logout/?$', views.logout, name='logout'),
    url(r'index/?$', login_required(views.IndexView.as_view(), login_url='/dashboard/login'), name='index'),
    url(r'test/?$', login_required(views.TestView.as_view(), login_url='/dashboard/login'), name='test'),
    url(r'test2/?$', login_required(views.Test2View.as_view(), login_url='/dashboard/login'), name='test2'),
    url(r'tables/?$', login_required(views.TablesView.as_view(), login_url='/dashboard/login'), name='tables'),
    url(r'dynamic/?$', views.TablesDynamicView.as_view(), name='tables_dynamic'),
    #url(r'dashboard/temp/?$', TempPlotView.as_view(), name='temp'),
]
