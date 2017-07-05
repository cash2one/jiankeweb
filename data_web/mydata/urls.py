from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from mydata.views import IndexView,\
        TempPlotView, people,\
        LoginView,\
        TablesView, TablesDynamicView

urlpatterns = [
    url(r'dashboard/login/?$', LoginView.as_view(), name='login'),
    url(r'dashboard/index/?$', login_required(IndexView.as_view(), login_url='/mydata/dashboard/login'), name='index'),
    url(r'dashboard/tables/?$', TablesView.as_view(), name='tables'),
    url(r'dashboard/dynamic/?$', TablesDynamicView.as_view(), name='tables_dynamic'),
    url(r'dashboard/temp/?$', TempPlotView.as_view(), name='temp'),
    url(r'dashboard/people/?$', people),
]
