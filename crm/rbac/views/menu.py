#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from rbac.forms.menu import MenuForm, SecondMenuForm
from rbac.models import Menu, Permission
from rbac.service.urls import memory_reverse


def menu_list(request):
    menus = Menu.objects.all()
    # 用户选择的一级菜单
    menu_id = request.GET.get('mid')
    # 用户选择的二级菜单
    second_menu_id = request.GET.get('sid')
    menu_exists = Menu.objects.filter(id=menu_id).exists()
    menu_id = menu_id if menu_exists else None
    if menu_id:
        second_menus = Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []
    result = {"menus": menus, "menu_id": menu_id, 'second_menus': second_menus, 'second_menu_id': second_menu_id, }

    return render(request, "menu_list.html", result)


def menu_add(request):
    if request.method == "GET":
        menu_form = MenuForm()
        return render(request, 'role_change.html', {'form': menu_form})
    menu_form = MenuForm(request.POST)
    if menu_form.is_valid():
        menu_form.save()
        return redirect(memory_reverse(request, "rbac:menu_list"))
    return render(request, 'rbac/change.html', {'form': menu_form})


def menu_edit(request, pk):
    obj = Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("一级菜单不存在")
    if request.method == "GET":
        menu_form = MenuForm(instance=obj)
        return render(request, "role_change.html", {'form': menu_form})
    menu_form = MenuForm(instance=obj, data=request.POST)
    if menu_form.is_valid():
        menu_form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, "role_change.html", {"form": menu_form})


def menu_del(request, pk):
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if request.method == "GET":
        return render(request, "role_delete.html", {'origin_url ': origin_url})
    obj = Menu.objects.filter(id=pk).delete()
    if not obj:
        return HttpResponse("一级菜单不存在")
    return redirect(origin_url)


def second_menu_add(request, menu_id):
    menu_object = Menu.objects.filter(id=menu_id).first()
    if request.method == "GET":
        menu_form = SecondMenuForm(initial={'menu': menu_object})
        return render(request, 'role_change.html', {'form': menu_form})
    menu_form = SecondMenuForm(request.POST)
    if menu_form.is_valid():
        menu_form.save()
        return redirect(memory_reverse(request, "rbac:menu_list"))
    return render(request, 'rbac/change.html', {'form': menu_form})


def second_menu_edit(request, pk):
    obj = Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("二级菜单不存在")
    if request.method == "GET":
        menu_form = SecondMenuForm(instance=obj)
        return render(request, "role_change.html", {'form': menu_form})
    menu_form = SecondMenuForm(instance=obj, data=request.POST)
    if menu_form.is_valid():
        menu_form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, "role_change.html", {"form": menu_form})


def second_menu_del(request, pk):
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if request.method == "GET":
        return render(request, "role_delete.html", {'origin_url ': origin_url})
    obj = Permission.objects.filter(id=pk).delete()
    if not obj:
        return HttpResponse("二级菜单不存在")
    return redirect(origin_url)
