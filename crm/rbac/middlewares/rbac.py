#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from django.http import HttpResponse

from crm import settings


class RbacMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def process_request(request):
        current_url = request.path_info
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):  # 白名单中的URL无需权限验证即可访问
                return None
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_list:
            return HttpResponse("未获取到用户权限信息,请登录!")
        flag = False
        for url in permission_list:
            reg = f"^{url}$"
            if re.match(reg, current_url):
                flag = True
                break
        if not flag:
            return HttpResponse("无权限访问")

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response
