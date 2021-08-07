#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from rbac.views import role, user
from web.views import customer, payment, account

app_name = 'rbac'
urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='role_list'),
    re_path(r'^role/add/$', role.role_add, name="role_add"),
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name="role_edit"),
    re_path(r'^role/del/(?P<pk>\d+)/$', role.role_del, name="role_del"),

    re_path(r'^user/list/$', user.user_list, name='user_list'),
    re_path(r'^user/add/$', user.user_add, name="user_add"),
    re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name="user_edit"),
    re_path(r'^user/del/(?P<pk>\d+)/$', user.user_del, name="user_del"),
    re_path(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name="user_reset_pwd")
]
