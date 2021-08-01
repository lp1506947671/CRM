#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse

from rbac.forms.role import RoleForm
from rbac.models import Role


def role_list(request):
    role_queryset = Role.objects.all()
    return render(request, "role_list.html", {'roles': role_queryset})


def role_add(request):
    if request.method == "GET":
        role_form = RoleForm()
        return render(request, 'role_change.html', {'form': role_form})
    role_form = RoleForm(request.POST)
    if role_form.is_valid():
        role_form.save()
        return redirect(reverse("rbac:role_list"))

    return render(request, 'role_change.html', {'form': "添加客户成功"})


def role_edit(request):
    ...
    return


def role_del(request):
    ...
    return
