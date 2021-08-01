#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import re_path

from rbac.views import role
from web.views import customer, payment, account

app_name = 'rbc'
urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='role_list'),
    re_path(r'^role/edit/$', role.role_edit, name="role_edit"),
    re_path(r'^role/del/$', role.role_del, name="role_del"),
    re_path(r'^role/add/$', role.role_add, name="role_add"),

]
