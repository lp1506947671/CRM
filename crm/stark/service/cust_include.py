#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from types import FunctionType

from django.conf.urls import url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe


class StarkHandler:
    display_list = []
    per_page_count = 1

    def __init__(self, model_class, prev):
        self.stark = stark
        self.model_class = model_class
        self.prev = prev

    def my_paginator(self, per_page, current_page):
        a = self.model_class.objects.all().order_by("pk")
        paginator1 = Paginator(a, per_page)

        current_page_num = int(current_page)
        try:
            current_page = paginator1.page(current_page_num)
            print("object_list", current_page.object_list)
        except EmptyPage as e:
            current_page = paginator1.page(1)
        except PageNotAnInteger as e:
            current_page = paginator1.page(paginator1.count)

        # 需求:总页数54,使其永远只显示11页
        if paginator1.num_pages > 11:
            if current_page_num - 5 < 1:
                page_range = range(1, 12)
            elif current_page_num + 5 > paginator1.num_pages:
                page_range = range(paginator1.num_pages - 10, paginator1.num_pages + 1)
            else:
                page_range = range(current_page_num - 5, current_page_num + 6)
        else:
            page_range = paginator1.page_range

        has_previous = current_page.has_previous()
        previous_page_number = 0
        if has_previous:
            previous_page_number = current_page.previous_page_number()
        has_next = current_page.has_next()
        next_page_number = 0
        if has_next:
            next_page_number = current_page.next_page_number()

        dict1 = {
            "start": current_page.start_index() - 1,
            "end": current_page.end_index(),
            "page_range": page_range,
            "current_page": current_page,
            "has_previous": has_previous,
            "previous_page_number": previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number

        }

        return dict1

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

    def get_list_display(self):
        """给予用户对表的列的自定义扩展,例如：根据用户的不同显示不同的列"""
        value = []
        value.extend(self.display_list)
        return value

    def add_view(self, request):
        return HttpResponse("增加")

    def delete_view(self, request, pk):
        return HttpResponse("删除")

    def change_view(self, request, pk):
        return HttpResponse("改变")

    def list_view(self, request):
        current_page_num = request.GET.get("page", 1)
        paginate_result = self.my_paginator(self.per_page_count, current_page_num)
        data_list = self.model_class.objects.all()[paginate_result["start"]: paginate_result["end"]]
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
        result = {'header_list': header_list,
                  'body_list': body_list,
                  "current_page_num": current_page_num
                  }
        result.update(paginate_result)
        return render(request, 'list.html', result)

    def url_name(self, name):
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return f"{app_label}_{model_name}_{self.prev}_{name}"
        return f"{app_label}_{model_name}_{name}"

    @staticmethod
    def extra_url():
        return []

    def get_urls(self):
        patterns = [
            url(r"^list/$", self.list_view, name=self.url_name("list")),
            url(r"^add/$", self.add_view, name=self.url_name("add")),
            url(r"^change/(\d+)$", self.change_view, name=self.url_name("change")),
            url(r"^del/(\d+)/$", self.delete_view, name=self.url_name("del")),
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
