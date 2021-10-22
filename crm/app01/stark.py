#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.http import HttpResponse
from app01 import models
from stark.service.cust_include import StarkHandler, stark


class DepartHandler(StarkHandler):
    display_list = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]


class UserInfoHandler(StarkHandler):
    display_list = ['name', 'age', 'email', 'depart', StarkHandler.display_edit, StarkHandler.display_del]


class HostHandler(StarkHandler):
    def extra_urls(self):
        """额外的增加URL"""
        return [
            url(r'^detail/(\d+)/$', self.detail_view)
        ]

    def detail_view(self, request, pk):
        return HttpResponse('详细页面')


stark.register(models.Depart, DepartHandler)
stark.register(models.UserInfo, UserInfoHandler)
stark.register(models.Host, HostHandler)
