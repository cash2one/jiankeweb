from django.conf.urls import url, include

from mydata.views import IndexView,\
        TempPlotView, people,\
        TablesView, TablesDynamicView

urlpatterns = [
    url(r'dashboard/index/?$', IndexView.as_view(), name='index'),
    url(r'dashboard/tables/?$', TablesView.as_view(), name='tables'),
    url(r'dashboard/dynamic/?$', TablesDynamicView.as_view(), name='tables_dynamic'),
    url(r'dashboard/temp/?$', TempPlotView.as_view(), name='temp'),
    url(r'dashboard/people/?$', people),
]
