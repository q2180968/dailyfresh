from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from dailyfresh_user.views import *
from dailyfresh_user.models import *
from django.db import transaction
from datetime import datetime


# 购物车视图
@login_decorator
def cart(req):
    uid = req.session['user_id']
    carts = CartInfo.objects.filter(user=uid)
    context = {'title': '购物车', 'cart_page': 1, 'carts': carts}
    return render(req, 'dailyfresh_order/cart.html', context)


# 添加至购物车视图
@login_decorator
def add_cart(req, gid, count):
    uid = req.session['user_id']
    gid = int(gid)
    count = int(count)
    carts = CartInfo.objects.filter(user=uid, goods=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    count = CartInfo.objects.filter(user=uid, ).count()
    return JsonResponse({'count': count})


# 删除购物车单个商品操作
@login_decorator
def delete_goods(req, gid):
    uid = req.session.get('user_id')
    cart = CartInfo.objects.filter(goods=gid, user=uid)
    cart.delete()
    # oid=1为删除操作，2为数量加操作，3为数量减操作
    return redirect('/daily_order/cart')


# 修改购物车商品数量操作
@login_decorator
def update_count(req, gid, count):
    uid = req.session.get('user_id')
    cart = CartInfo.objects.get(user=uid, goods=gid)
    cart.count = count
    cart.save()
    return JsonResponse({'count': cart.count})


# 订单确认页面
@login_decorator
def order(req):
    if req.method == 'GET':
        return redirect('/daily_order/cart')
    post = req.POST
    cart_goods_id = post.getlist('carts_goods_id')
    uid = req.session['user_id']
    user = userinfo.objects.get(id=uid)
    address = user.uaddress
    carts = CartInfo.objects.filter(goods_id__in=cart_goods_id, user=uid)
    # order = OrderInfo()
    # now = datetime.now()
    # order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
    # order.user_id = uid
    # order.save()
    context = {'title': '提交订单', 'page_user': 1, 'address': address, 'carts': carts}
    return render(req, 'dailyfresh_order/place_order.html', context)


'''
实务操作，一旦操作失败全部回退
1、创建订单对象
2、判断商品的库存
3、创建详单对象
4、修改商品库存
5、删除购物车
'''


@login_decorator
@transaction.atomic()
# @transaction.Atomic
def order_handle(req):
    # 保存一个事物点
    tran_id = transaction.savepoint()
    try:
        if req.method == 'GET':
            return redirect('/daily_order/cart')
        uid = req.session['user_id']
        order = OrderInfo()
        now = datetime.now()
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.save()
        post = req.POST
        # 获取用户
        uid = req.session['user_id']
        user = userinfo.objects.get(id=uid)
        # 获取传递过来的购物车信息
        cart_ids = post.getlist('cart_id')
        carts = CartInfo.objects.filter(id__in=cart_ids)
        # 获取地址和订单编号h
        address = post.get('address')
        order = OrderInfo()
        now = datetime.now()
        oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.oid = oid
        order.user_id = uid
        order.oaddress = address
        total = post.get('total')
        order.ototal = total
        order.save()
        for cart in carts:
            good = GoodsInfo.objects.get(id=cart.goods_id)
            if int(good.gkuncun) >= cart.count:
                good.gkuncun -= 1
                good.save()

                detail = OrderDetail()
                detail.goods_id = good.id
                detail.order_id = order.oid
                detail.price = good.gprice
                detail.count = cart.count
                detail.save()

                cart.delete()
            else:
                # 如果操作失败，回滚并提供错误代码
                transaction.savepoint_rollback(tran_id)
                # return HttpResponse({'status': 2})
                return HttpResponse("出错啦，库存不足")
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(tran_id)
        # return HttpResponse({'status': 3})
        return HttpResponse("出错啦！购物车之前出的错")

    # return HttpResponse({'status': 1})
    return redirect('df_user/order/')
