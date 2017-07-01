from django.conf.urls import url

from mydata.views import weather_chart_view

urlpatterns = [
    url(r'line/charts/?', weather_chart_view),
]
