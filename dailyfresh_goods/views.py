from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from dailyfresh_order.models import *
import dailyfresh_order
from dailyfresh_user.models import *


# 首页视图
def index(req):
    uid = req.session.get('user_id')
    carts_count = dailyfresh_order.models.CartInfo.objects.filter(user=uid).count()
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'goods_info': 1, 'title': '首页',
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               'count': carts_count
               }
    return render(req, 'dailyfresh_goods/index.html', context)


# 详情页视图
def detail(req, gid):
    uid = req.session.get('user_id')
    carts_count = dailyfresh_order.models.CartInfo.objects.filter(user=uid).count()
    goods = GoodsInfo.objects.get(id=gid)
    goods.gclick += 1
    goods.save()
    new_goods = GoodsInfo.objects.filter(gtype=goods.gtype_id).order_by('-id')[0:2]
    context = {'goods_info': 1, 'title': '商品详情', 'goods': goods, 'new_goods': new_goods, 'count': carts_count}
    response = render(req, 'dailyfresh_goods/detail.html', context)
    # 最近浏览
    goods_ids = req.COOKIES.get('goods_ids', '')
    goods_id = '%d' % goods.id
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id) > 0:
            goods_ids1.remove(goods_id)  # 如果已经存在，将原来记录删除
        goods_ids1.insert(0, goods_id)  # 将商品添加到第一位
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        print(goods_ids1)
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id  # 如果没有任何浏览直接添加
    response.set_cookie('goods_ids', goods_ids)  # 写入COOKIES
    return response


# 列表页视图
def list(req, tid, pindex, order_type):
    goods = None
    if order_type == '1':
        goods = GoodsInfo.objects.filter(gtype=tid)
    if order_type == '2':
        goods = GoodsInfo.objects.filter(gtype=tid).order_by('gclick')
    if order_type == '3':
        goods = GoodsInfo.objects.filter(gtype=tid).order_by('gprice')
    page = Paginator(goods, 15)
    cur_type = TypeInfo.objects.get(id=tid)
    new_goods = GoodsInfo.objects.filter(gtype_id=tid).order_by('-id')[0:2]
    if pindex == '':
        pindex = 1
    cur_page = page.page(int(pindex))
    total_page = page.page_range
    context = {'page_user': 1, 'title': '列表页',
               'total_page': total_page, 'cur_page': cur_page,
               'cur_type': cur_type, 'new_goods': new_goods,
               'pindex': pindex, 'order_type': order_type}
    return render(req, 'dailyfresh_goods/list.html', context)
