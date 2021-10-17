#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.http import HttpResponse

from app01 import models
from stark.service.cust_include import StarkHandler, stark


class DepartHandler(StarkHandler):

    def extra_urls(self):
        """
        额外的增加URL
        :return:
        """
        return [
            url(r'^detail/(\d+)/$', self.detail_view)
        ]

    def detail_view(self, request, pk):
        return HttpResponse('详细页面')


class UserInfoHandler(StarkHandler):

    def get_urls(self):
        """
        修改URL
        :return:
        """
        patterns = [
            url(r'^list/$', self.list_view),
            url(r'^add/$', self.add_view),
        ]

        return patterns


class HostHandler(StarkHandler):
    pass


stark.register(models.Depart, DepartHandler)
stark.register(models.UserInfo, UserInfoHandler)
stark.register(models.Host, HostHandler)
