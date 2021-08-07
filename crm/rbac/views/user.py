#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from rbac.forms.user import UserModelForm, UpdateUserModelForm, ResetPasswordUserModelForm
from rbac.models import UserInfo


def user_list(request):
    user_queryset = UserInfo.objects.all()
    return render(request, "user_list.html", {'users': user_queryset})


def user_add(request):
    if request.method == "GET":
        user_form = UserModelForm()
        return render(request, 'role_change.html', {'form': user_form})
    user_form = UserModelForm(request.POST)
    if user_form.is_valid():
        user_form.save()
        return redirect(reverse("rbac:user_list"))

    return render(request, 'role_change.html', {'form': user_form})


def user_edit(request, pk):
    obj = UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("角色不存在")
    if request.method == "GET":
        user_form = UpdateUserModelForm(instance=obj)
        return render(request, "role_change.html", {'form': user_form})
    user_form = UpdateUserModelForm(instance=obj, data=request.POST)
    if user_form.is_valid():
        user_form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, "role_change.html", {"form": user_form})


def user_del(request, pk):
    origin_url = reverse("rbac:user_list")
    if request.method == "GET":
        return render(request, "role_delete.html", {'origin_url ': origin_url})
    obj = UserInfo.objects.filter(id=pk).delete()
    if not obj:
        return HttpResponse("角色不存在")
    return redirect(origin_url)


def user_reset_pwd(request, pk):
    obj = UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("角色不存在")
    if request.method == "GET":
        user_form = ResetPasswordUserModelForm(instance=obj)
        return render(request, "role_change.html", {'form': user_form})
    user_form = ResetPasswordUserModelForm(instance=obj, data=request.POST)
    if user_form.is_valid():
        user_form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, "role_change.html", {"form": user_form})
