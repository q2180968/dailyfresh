from django.db import models


# from dailyfresh_user.views import *


# 购物车模型
class CartInfo(models.Model):
    user = models.ForeignKey('dailyfresh_user.userinfo', blank=True, null=True, on_delete=models.SET_NULL)
    goods = models.ForeignKey('dailyfresh_goods.GoodsInfo', blank=True, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField()

    class Meta():
        db_table = 'cartinfo'


# 订单类
class OrderInfo(models.Model):
    oid = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey('dailyfresh_user.userinfo', on_delete=models.CASCADE)
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    oaddress = models.CharField(max_length=200, default="")


# 订单详情类
class OrderDetail(models.Model):
    goods = models.ForeignKey('dailyfresh_goods.GoodsInfo', on_delete=models.CASCADE)
    order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.IntegerField()
