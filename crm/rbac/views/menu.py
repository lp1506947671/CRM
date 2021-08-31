#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rbac.forms.menu import MenuForm, SecondMenuForm, PermissionMenuForm
from rbac.models import Menu, Permission
from rbac.service.routers import get_all_url_dict
from rbac.service.urls import memory_reverse


def menu_list(request):
    menus = Menu.objects.all()

    # 用户选择的一级菜单
    menu_id = request.GET.get('mid')
    menu_exists = Menu.objects.filter(id=menu_id).exists()
    menu_id = menu_id if menu_exists else None
    second_menus = Permission.objects.filter(menu_id=menu_id) if menu_id else []

    # 用户选择的二级菜单
    second_menu_id = request.GET.get('sid')
    second_menu_exists = Permission.objects.filter(id=second_menu_id).exists()
    second_menu_id = None if not second_menu_exists else second_menu_id
    permissions = Permission.objects.filter(pid_id=second_menu_id) if second_menu_id else []

    result = {"menus": menus,
              "menu_id": menu_id,
              'second_menus': second_menus,
              'second_menu_id': second_menu_id,
              'permission': permissions
              }

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


def permission_add(request, second_menu_id):
    second_menu_object = Permission.objects.filter(id=second_menu_id).first()
    if not second_menu_object:
        return HttpResponse('二级菜单不存在，请重新选择！')
    if request.method == "GET":
        second_menu_form = PermissionMenuForm()
        return render(request, 'role_change.html', {'form': second_menu_form})

    second_menu_form = PermissionMenuForm(request.POST)
    if second_menu_form.is_valid():
        second_menu_form.instance.pid = second_menu_object
        second_menu_form.save()
        return redirect(memory_reverse(request, "rbac:menu_list"))
    return render(request, 'rbac/change.html', {'form': second_menu_form})


def permission_edit(request, pk):
    obj = Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("权限不存在")
    if request.method == "GET":
        menu_form = PermissionMenuForm(instance=obj)
        return render(request, "role_change.html", {'form': menu_form})
    menu_form = PermissionMenuForm(instance=obj, data=request.POST)
    if menu_form.is_valid():
        menu_form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, "role_change.html", {"form": menu_form})


def permission_del(request, pk):
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if request.method == "GET":
        return render(request, "role_delete.html", {'origin_url ': origin_url})
    obj = Permission.objects.filter(id=pk).delete()
    if not obj:
        return HttpResponse("权限不存在")
    return redirect(origin_url)


def multi_permissions(request):
    result = get_all_url_dict()

    return HttpResponse("ok")
