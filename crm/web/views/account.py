#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from rbac import models
from rbac.service.init_permission import init_permission


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})
    init_permission(current_user, request)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request.session[now] = {"is_login": True, "username": current_user.name, "last_visit_time": now}
    response2 = HttpResponseRedirect('/customer/list/')
    response2.set_cookie("session_id", now)
    return response2


def logout(request):
    session_id = request.COOKIES.get("sessionid")
    request.session.flush()
    response1 = HttpResponseRedirect('/login/')
    response1.delete_cookie(session_id)
    return response1
