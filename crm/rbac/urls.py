#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path
from rbac.views import role, user, menu

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
    re_path(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name="user_reset_pwd"),

    re_path(r'^menu/list/$', menu.menu_list, name='menu_list'),
    re_path(r'^menu/add/$', menu.menu_add, name='menu_add'),
    re_path(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name='menu_edit'),
    re_path(r'^menu/del/(?P<pk>\d+)/$', menu.menu_del, name='menu_del'),

    re_path(r'^second/menu/add/(?P<menu_id>\d+)$', menu.second_menu_add, name='second_menu_add'),
    re_path(r'^second/menu/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    re_path(r'^second/menu/del/(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),
]
