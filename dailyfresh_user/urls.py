from django.contrib import admin
from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'df_user/register/$', register),
    url(r'df_user/register_handle/$', register_handle),
    url(r'df_user/user_validate/(\w+)', user_validate),
    url(r'df_user/login/$', login),
    url(r'df_user/login_handle/$', login_handle),
    url(r'df_user/info/$', user_info),
    url(r'df_user/order/$', order),
    url(r'df_user/center_site/$', center_site),
    url(r'df_user/center_site_handle/$', center_site_handle),
    url(r'df_user/logout/$', logout),
]
