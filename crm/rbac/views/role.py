#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render

from rbac.models import Role


def role_list(request):
    role_queryset = Role.objects.all()
    return render(request, "role_list.html", {'roles': role_queryset})


def role_edit(request):
    ...
    return


def role_del(request):
    ...
    return


def role_add(request):
    ...
    return render(request, 'role_change.html', {'form': "添加客户成功"})
