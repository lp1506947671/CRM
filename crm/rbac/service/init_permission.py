#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from crm import settings


def init_permission(current_user, request):
    # 获取当前用户所有权限
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__title",
                                                                                      "permissions__url",
                                                                                      "permissions__name",
                                                                                      "permissions__menu_id",
                                                                                      "permissions__pid_id",
                                                                                      "permissions__pid__title",
                                                                                      "permissions__pid__url",
                                                                                      "permissions__menu__title",
                                                                                      "permissions__menu__icon"
                                                                                      ).distinct()

    permission_dict = {}
    menu_dict = {}
    for item in permission_queryset:
        permission_dict[item["permissions__name"]] = {'id': item["permissions__id"],
                                                      "title": item["permissions__title"],
                                                      'url': item["permissions__url"],
                                                      "pid": item["permissions__pid_id"],
                                                      'p_title': item['permissions__pid__title'],
                                                      'p_url': item['permissions__pid__url'], }
        menu_id = item["permissions__menu_id"]
        if not menu_id:
            continue
        node = {"id": item["permissions__id"], "title": item["permissions__title"], "url": item["permissions__url"]}
        if menu_id in menu_dict:
            menu_dict[menu_id]["children"].append(node)
        else:
            menu_dict[menu_id] = {
                "title": item["permissions__menu__title"],
                "icon": item["permissions__menu__icon"],
                'children': [node, ]
            }

    # 根据当前用户信息获取此用户所拥有的所有权限,并放入session
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
