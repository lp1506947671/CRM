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
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse("未获取到用户权限信息,请登录!")
        url_record = [{"title": "首页", "url": "#"}]
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

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response
