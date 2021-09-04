#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rbac.forms.menu import MenuForm, SecondMenuForm, PermissionMenuForm, MultiAddPermission, MultiEditPermission
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
    """批量操作权限"""
    """
    router_url_dict格式
       {
           'rbac:role_list':{'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
           'rbac:role_add':{'name': 'rbac:role_add', 'url': '/rbac/role/add/'},
           ....
       }
    router_name_set格式   
    {
        'rbac:role_list': {'id':1,'title':'角色列表',name:'rbac:role_list',url.....},
        'rbac:role_add': {'id':1,'title':'添加角色',name:'rbac:role_add',url.....},
        ...
    } 
    values:
    <QuerySet [(‘红楼梦’, 300), (‘水浒传’, 200)]>  
    values_list:
    <QuerySet [{‘book__title’: ‘红楼梦’, ‘book__price’: 300}, {‘book__title’: ‘水浒传’, ‘book__price’: 200}]>
       """
    #  1.获取项目中所有的router_url
    router_url_dict = get_all_url_dict()
    #  2. 获取所有router_url的别名
    router_name_set = set(router_url_dict.keys())

    #  3.获取Permission中所有的权限并将permission中权限存到permission_name_set和permission_dict中
    permissions = Permission.objects.all().values("id", "title", "url", "name", "menu_id", "pid_id")
    permission_dict = OrderedDict()
    permission_name_set = set()
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])

    #  4.遍历permission_dict并且判断是路由和数据库中都存在但是不相等的情况
    for name, value in permission_dict.items():
        router_url_row = router_url_dict.get(name)
        if not router_url_row:
            continue
        if value['url'] != router_url_row["url"]:
            value['url'] = "路由和数据库中的不一致"

    # 计算应该增加的name:+
    generate_name_list = router_name_set - permission_name_set
    # 创建表单集 formset_factory:MultiAddPermission
    generate_formset_class = formset_factory(MultiAddPermission, extra=0)
    # 生成表单集 generate_formset_class:initial
    generate_formset = generate_formset_class(
        initial=[row_dict for name, row_dict in router_url_dict.items() if name in generate_name_list])

    # 计算应该删除的name:-
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]
    # 计算应该更新的name:&
    update_list = permission_name_set & router_name_set
    # 创建表单集 formset_factory:MultiEditPermission
    update_formset_class = formset_factory(MultiEditPermission, extra=0)
    # 生成表单集 update_formset_class:initial
    update_formset = update_formset_class(
        initial=[row_dict for name, row_dict in router_url_dict.items() if name in update_list])

    result = {
        "generate_formset": generate_formset,
        "delete_row_list": delete_row_list,
        "update_formset": update_formset
    }

    return render(request, "multi_permissions.html", result)
