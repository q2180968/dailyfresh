from django.contrib import admin
from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^index/', index),
    url(r'daily_goods/detail/(\d+)', detail),
    url(r'daily_goods/list(\d+)_(\d+)_(\d+)', list),
]
