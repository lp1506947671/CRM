#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
from types import FunctionType

from django import forms
from django.conf.urls import url
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from stark.utils.pagination import Pagination


class StarkModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StarkModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class StarkHandler:
    display_list = []
    per_page_count = 1
    has_add_btn = True  # 是否启用添加按钮
    model_form_class = None

    def __init__(self, model_class, prev):
        self.stark = stark
        self.model_class = model_class
        self.prev = prev
        self.request = None

    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        class DynamicModelForm(StarkModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm

    def reverse_add_url(self):
        name = f"{self.stark.namespace}:{self.url_name('add')}"
        base_url = reverse(name)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = f"{base_url}?{new_query_dict.urlencode()}"
        return add_url

    def reverse_list_url(self):
        name = f"{self.stark.namespace}:{self.url_name('list')}"
        base_url = reverse(name)
        param = self.request.GET.get('_filter')
        if not param:
            return base_url
        return f"{base_url}?{param}"

    def save(self, form, is_update=False):
        """在使用ModelForm保存数据之前预留的钩子方法"""
        form.save()

    def get_add_btn(self):
        if self.has_add_btn:
            return "<a class='btn btn-primary' href='%s'>添加</a>" % self.reverse_add_url()
        return None

    def get_list_display(self):
        """给予用户对表的列的自定义扩展,例如：根据用户的不同显示不同的列"""
        value = []
        value.extend(self.display_list)
        return value

    def display_edit(self, obj=None, is_header=None):
        if is_header:
            return "编辑"
        name = f"{self.stark.namespace}:{self.url_name('change')}"
        return mark_safe(f'<a href="{reverse(name, args=(obj.pk,))}">编辑</a>')

    def display_del(self, obj=None, is_header=None):
        if is_header:
            return "删除"
        name = f"{self.stark.namespace}:{self.url_name('del')}"
        return mark_safe(f'<a href="{reverse(name, args=(obj.pk,))}">删除</a>')

    def add_view(self, request):
        model_form_class = self.get_model_form_class()
        if request.method == 'GET':
            form = model_form_class()
            return render(request, 'change.html', {'form': form})
        form = model_form_class(data=request.POST)
        if form.is_valid():
            self.save(form, is_update=False)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_list_url())
        return render(request, 'change.html', {'form': form})

    def delete_view(self, request, pk):
        return HttpResponse("删除")

    def change_view(self, request, pk):
        return HttpResponse("改变")

    def list_view(self, request):
        all_count = self.model_class.objects.all().count()
        current_page_num = request.GET.get("page", 1)
        query_params = request.GET.copy()
        query_params._mutable = True
        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )
        data_list = self.model_class.objects.all()[pager.start:pager.end]
        display_columns = self.get_list_display()
        # 获取表头
        header_list = []
        for key_or_func in display_columns:
            if isinstance(key_or_func, FunctionType):
                header_list.append(key_or_func(self, obj=None, is_header=True))
                continue
            if display_value := self.model_class._meta.get_field(key_or_func).verbose_name:
                header_list.append(display_value)
        # 获取表内容
        body_list = []
        for row in data_list:
            tr_list = []
            if display_columns:
                for key_or_func in display_columns:
                    if isinstance(key_or_func, FunctionType):
                        tr_list.append(key_or_func(self, row, is_header=False))
                        continue
                    if row_item := getattr(row, key_or_func):
                        tr_list.append(row_item)
            else:
                # 征集dispaly_list没有配置的情况下的处理
                tr_list.append(row)

            body_list.append(tr_list)
        # 添加按钮
        add_btn = self.get_add_btn()
        result = {'header_list': header_list,
                  'body_list': body_list,
                  "current_page_num": current_page_num,
                  'pager': pager,
                  'add_btn': add_btn
                  }
        return render(request, 'list.html', result)

    def url_name(self, name):
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return f"{app_label}_{model_name}_{self.prev}_{name}"
        return f"{app_label}_{model_name}_{name}"

    @staticmethod
    def extra_url():
        return []

    def wrapper(self, func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)

        return inner

    def get_urls(self):
        patterns = [
            url(r"^list/$", self.wrapper(self.list_view), name=self.url_name("list")),
            url(r"^add/$", self.wrapper(self.add_view), name=self.url_name("add")),
            url(r"^change/(\d+)$", self.wrapper(self.change_view), name=self.url_name("change")),
            url(r"^del/(\d+)/$", self.wrapper(self.delete_view), name=self.url_name("del")),
        ]
        patterns.extend(self.extra_url())
        return patterns


class Stark:
    def __init__(self):
        self.app_name = 'stark'
        self.namespace = 'stark'
        self._register = []

    def register(self, model_class, handler_class=None, prev=None):
        handler_class = StarkHandler if not handler_class else handler_class
        self._register.append(
            {'model_class': model_class, 'handler_class': handler_class(model_class, prev), "prev": prev})

    def get_urls(self):
        patterns = []
        for item in self._register:
            model_class = item["model_class"]
            handler_class = item['handler_class']
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name
            url_path = f"{app_label}/{model_name}/"
            if prev := item["prev"]:
                url_path = f"{app_label}/{model_name}/{prev}/"
            my_include = (handler_class.get_urls(), None, None)
            my_url = url(url_path, my_include)
            patterns.append(my_url)

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace


stark = Stark()
