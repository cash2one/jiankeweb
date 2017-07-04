from django.conf.urls import url, include

from mydata.views import IndexView, TempPlotView

urlpatterns = [
    url(r'dashboard/index/?', IndexView.as_view(), name='index'),
    url(r'dashboard/temp/?', TempPlotView.as_view(), name='temp'),
]
