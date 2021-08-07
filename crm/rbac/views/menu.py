#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from rbac.forms.menu import MenuForm
from rbac.models import Menu
from rbac.service.urls import memory_reverse


def menu_list(request):
    menus = Menu.objects.all()
    menu_id = request.GET.get('mid')
    return render(request, "menu_list.html", {"menus": menus, "menu_id": menu_id})


def menu_add(request):
    if request.method == "GET":
        menu_form = MenuForm()
        return render(request, 'role_change.html', {'form': menu_form })
    menu_form = MenuForm(request.POST)
    if menu_form .is_valid():
        menu_form .save()
        return redirect(memory_reverse(request,"rbac:menu_list"))
    return render(request, 'rbac/change.html', {'form': menu_form })


def menu_edit(request,pk):
    obj = Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("一级菜单不存在")
    if request.method == "GET":
        menu_form  = MenuForm(instance=obj)
        return render(request, "role_change.html", {'form': menu_form })
    menu_form  = MenuForm(instance=obj, data=request.POST)
    if menu_form .is_valid():
        menu_form .save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, "role_change.html", {"form": menu_form })


def menu_del(request, pk):
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if request.method == "GET":
        return render(request, "role_delete.html", {'origin_url ': origin_url})
    obj = Menu.objects.filter(id=pk).delete()
    if not obj:
        return HttpResponse("一级菜单不存在")
    return redirect(origin_url)
