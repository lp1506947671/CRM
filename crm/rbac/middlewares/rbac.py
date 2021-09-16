#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from django.http import HttpResponse
from django.shortcuts import redirect

from crm import settings


class RbacMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        request.current_selected_permission = None
        request.url_record = []
        my_response = self.get_response(request)

        current_url = request.path_info
        # 访问127.0.0.1:8080页面时直接跳转到登录界面
        if current_url == "/":
            return redirect("/login/")

        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):  # 白名单中的URL无需权限验证即可访问
                return my_response
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        if not permission_dict:
            print("未获取到用户权限信息,请登录!")
            return redirect("/login/")
        url_record = [{"title": "首页", "url": "#"}]

        # 此处代码进行判断
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, request.path_info):
                # 需要登录，但无需权限校验
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                return my_response
        flag = False

        for item in permission_dict.values():
            reg = f"^{item['url']}$"
            if re.match(reg, current_url):
                request.current_selected_permission = item['pid'] or item['id']
                if item["pid"]:
                    url_record.extend([{"title": item['p_title'], "url": item['p_url']},
                                       {"title": item['title'], "url": item['url'], "class": "active"}
                                       ])
                else:
                    url_record.extend([
                        {"title": item['title'], "url": item['url'], "class": "active"}
                    ])
                flag = True
                break
        request.url_record = url_record
        if not flag:
            return HttpResponse("无权限访问")
        return my_response

    def __call__(self, request):
        response = self.process_request(request)
        return response
