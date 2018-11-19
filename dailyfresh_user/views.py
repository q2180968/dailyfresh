from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from hashlib import sha1
from dailyfresh_goods.models import *

from dailyfresh_order.models import OrderInfo, OrderDetail


# 用户登录验证装饰器
def login_decorator(func):
    def login_fun(req, *args, **kwargs):
        if req.session.has_key('user_id'):
            return func(req, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/df_user/login/')
            red.set_cookie('url', req.get_full_path())
            return red

    return login_fun


# 注册视图
def register(req):
    content = {'title': '注册'}
    return render(req, 'dailyfresh_user/register.html', content)


# 注册执行视图
def register_handle(req):
    post = req.POST
    uname = post['user_name']
    upwd = post['pwd']
    ucpwd = post['cpwd']
    uemail = post['email']
    count = userinfo.objects.filter(uname=uname).count()
    if count != 1:
        user = userinfo()
        user.uname = uname
        s1 = sha1()
        s1.update(upwd.encode('UTF8'))
        user.upwd = s1.hexdigest()
        user.uemail = uemail
        user.save()
        return redirect('/df_user/login')
    return redirect('/df_user/register')


# 用户名重复验证
def user_validate(req, username):
    count = userinfo.objects.filter(uname=username).count()
    if count == 1:
        return JsonResponse({'data': count})


# 登录视图
def login(req):
    uname = req.COOKIES.get('uname', '')
    print(uname)
    content = {'title': '登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(req, 'dailyfresh_user/login.html', content)


# 登录操作视图
def login_handle(req):
    post = req.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jiezhu = post.get('jiezhu', 0)
    user = userinfo.objects.filter(uname=uname)
    if len(user) == 1:
        s1 = sha1()
        s1.update(upwd.encode('UTF8'))
        if s1.hexdigest() == user[0].upwd:
            url = req.COOKIES.get('url', '/index/')
            red = HttpResponseRedirect(url)
            if jiezhu != 1:
                red.set_cookie('uname', uname)  # cookie记住用户名
                print('记录用户名')
            else:
                red.set_cookie('uname', '', max_age=-1)  # 取消cookie
            req.session['user_id'] = user[0].id
            req.session['user_name'] = user[0].uname
            print('登录成功')
            return red
        else:
            print('密码错误')
            content = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(req, 'dailyfresh_user/login.html', content)
    else:
        print('用户名错误')
        content = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(req, 'dailyfresh_user/login.html', content)


# 用户中心视图
@login_decorator
def user_info(req):
    uname = req.session['user_name']
    email = userinfo.objects.get(id=req.session['user_id']).uemail

    # 获取最近浏览记录
    goods_ids = req.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    if goods_ids == '':
        goods_list = []
    else:
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心', 'uname': uname, 'uemail': email, 'page_user': 1, 'goods_list': goods_list}
    return render(req, 'dailyfresh_user/user_center_info.html', context)


# 用户订单
@login_decorator
def order(req):
    uid = req.session['user_id']
    order = OrderInfo.objects.filter(user=uid)
    print(order)
    context = {'title': '用户中心', 'page_user': 1, 'orders': order}
    return render(req, 'dailyfresh_user/user_center_order.html', context)


# 用户收货地址
@login_decorator
def center_site(req):
    uname = req.session['user_name']
    uid = req.session['user_id']
    user = userinfo.objects.get(id=uid)
    address = user.uaddress + ' ' + user.urecvName + '收，电话：' + user.utelphone + ' 邮政编码：' + user.upostid
    context = {'title': '用户中心', 'uname': uname, 'user_id': uid, 'address': address, 'page_user': 1}
    return render(req, 'dailyfresh_user/user_center_site.html', context)


# 用户收货地址操作视图
def center_site_handle(req):
    post = req.POST
    uid = post.get('uid')
    recvname = post.get('recvname')
    address = post.get('address')
    postid = post.get('postid')
    telphone = post.get('telphone')
    print(uid)
    user = userinfo.objects.get(id=uid)
    user.urecvName = recvname
    user.uaddress = address
    user.upostid = postid
    user.utelphone = telphone
    user.save()
    return redirect('/df_user/center_site/')


# 登出操作
def logout(req):
    req.session.flush()
    return redirect('/index/')
