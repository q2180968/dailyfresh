from django.contrib import admin
from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'daily_order/cart', cart),
    url(r'daily_order/add_cart_(\d+)_(\d+)', add_cart),
    url(r'daily_order/delete_goods_(\d+)', delete_goods),
    url(r'daily_order/update_count(\d+)_(\d+)', update_count),
    url(r'daily_order/order/', order),
    url(r'daily_order/order_handle', order_handle),
]
