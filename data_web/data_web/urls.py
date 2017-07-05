from django.contrib import admin
from django.conf.urls import url, include

import  mydata

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mydata/', include('mydata.urls', namespace='mydata')),
]
