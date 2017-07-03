from django.conf.urls import url, include

from mydata.views import IndexView

urlpatterns = [
    url(r'dashboard/index/?', IndexView.as_view(), name='index'),
]
