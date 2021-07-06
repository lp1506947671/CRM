#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse, render,redirect

from rbac import models


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    # 根据当前用户信息获取此用户所拥有的所有权限，并放入session。

    # 当前用户所有权限
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__url").distinct()

    # 获取权限中所有的URL
    # permission_list = []
    # for item in permission_queryset:
    #     permission_list.append(item['permissions__url'])

    permission_list = [item['permissions__url'] for item in permission_queryset]
    request.session['luffy_permission_url_list_key'] = permission_list

    return redirect('/customer/list/')
