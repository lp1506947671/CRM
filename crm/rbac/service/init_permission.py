#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from crm import settings


def init_permission(current_user, request):
    # 当前用户所有权限
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__url").distinct()
    permission_list = [item['permissions__url'] for item in permission_queryset]
    # 根据当前用户信息获取此用户所拥有的所有权限,并放入session
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
