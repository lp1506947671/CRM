#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from crm import settings


def init_permission(current_user, request):
    # 获取当前用户所有权限
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__title",
                                                                                      "permissions__url",
                                                                                      "permissions__is_menu",
                                                                                      "permissions__icon"
                                                                                      ).distinct()
    menu_list = []
    permission_list = []
    for item in permission_queryset:
        if item["permissions__is_menu"]:
            menu_list.append({
                "title": item["permissions__title"],
                "icon": item["permissions__icon"],
                "url": item["permissions__url"],
            })
            permission_list.append(item["permissions__url"])
    # 根据当前用户信息获取此用户所拥有的所有权限,并放入session
    request.session[settings.MENU_SESSION_KEY] = menu_list
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
