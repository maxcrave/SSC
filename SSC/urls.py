"""SSC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^ssc/0', views.ssc_calculate_ssc),
    url(r'^ssc/hou', views.ssc_hou),
    url(r'^ssc/zhong', views.ssc_zhong),
    url(r'^ssc/qian', views.ssc_qian),
    url(r'^ssc/7', views.ssc_housan_yuce),
    url(r'^ssc/3', views.ssc_sixing),
    url(r'^ssc/4', views.make_sscnumber),
    url(r'^ssc/5', views.ssc_erxing),
    url(r'^ssc/6', views.make_sanxing),
]
