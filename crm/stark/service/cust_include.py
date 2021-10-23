#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
from types import FunctionType

from django import forms
from django.conf.urls import url
from django.db.models import Q, ForeignKey, ManyToManyField
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from stark.utils.pagination import Pagination


class Option:
    def __init__(self, filed, condition=None, value_name=None, text_func=None):
        self.filed = filed
        self.condition = condition or {}
        self.text_func = text_func
        self.is_choice = False
        self.value_name = value_name

    def get_condition(self, request, *args, **kwargs):
        return self.condition

    def run(self, model_class, request, *args, **kwargs):
        field_obj = model_class._meta.get_field(self.filed)
        verbose_name = field_obj.verbose_name
        if isinstance(field_obj, ForeignKey) or isinstance(field_obj, ManyToManyField):
            db_condition = self.get_condition(request, *args, **kwargs)
            search_group_list = field_obj.model.objects.filter(**db_condition).values_list(self.value_name).distinct()
            search_group_list = [item[0] for item in search_group_list]
        else:
            self.is_choice = True
            search_group_list = field_obj.choices

        return SearchGroupItem(verbose_name, self.get_text(search_group_list))

    def get_text(self, search_group_list):
        if self.text_func:
            return [self.text_func(item) for item in search_group_list]
        if self.is_choice:
            return [item[1] for item in search_group_list]
        return [str(item) for item in search_group_list]


class SearchGroupItem:
    def __init__(self, title, search_group_list):
        self.title = title
        self.search_group_list = search_group_list

    def __iter__(self):
        button_html = '<li><a class="btn btn-default btn-sm" href="%s" role="button" >%s</a></li>'
        yield '<ul class="list-inline">'
        yield f'<li><strong>{self.title}</strong></li>'
        yield button_html % ('#', '全部')
        for item in self.search_group_list:
            yield button_html % ('#', item)
        yield '</ul>'


class StarkModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StarkModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class StarkHandler:
    display_list = []
    per_page_count = 10
    has_add_btn = True  # 是否启用添加按钮
    model_form_class = None
    order_list = []
    search_list = []  # 查询字段
    action_list = []
    search_group = []

    def __init__(self, model_class, prev):
        self.stark = stark
        self.model_class = model_class
        self.prev = prev
        self.request = None

    def get_search_group(self):
        return self.search_group

    def get_action_list(self):
        return self.action_list

    def get_search_list(self):
        return self.search_list

    def get_order_list(self):
        return self.order_list or ['-id', ]

    def get_add_btn(self):
        if self.has_add_btn:
            return "<a class='btn btn-primary' href='%s'>添加</a>" % self.reverse_add_url()
        return None

    def get_list_display(self):
        """给予用户对表的列的自定义扩展,例如：根据用户的不同显示不同的列"""
        value = []
        value.extend(self.display_list)
        return value

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

    def action_multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()

    action_multi_delete.text = "批量删除"

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

    def display_checkbox(self, obj=None, is_header=None):
        if is_header:
            return "选择"
        return mark_safe(f'<input type="checkbox" name="pk" value="{obj.pk}">')

    def add_view(self, request):
        model_form_class = self.get_model_form_class()
        if request.method == 'GET':
            form = model_form_class()
            return render(request, 'change.html', {'form': form})
        data = request.POST.copy()
        # data._mutable = True
        # data['sex'] = int(data['sex'])
        form = model_form_class(data=data)
        if form.is_valid():
            self.save(form, is_update=False)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_list_url())
        return render(request, 'change.html', {'form': form})

    def delete_view(self, request, pk):
        origin_list_url = self.reverse_list_url()
        if request.method == 'GET':
            return render(request, 'delete.html', {'cancel': origin_list_url})
        self.model_class.objects.filter(pk=pk).delete()
        return redirect(origin_list_url)

    def change_view(self, request, pk, *args, **kwargs):
        current_change_obj = self.model_class.objects.filter(pk=pk).first()
        if not current_change_obj:
            return HttpResponse('要修改的数据不存在，请重新选择！')
        model_form_class = self.get_model_form_class()
        if request.method == 'GET':
            form = model_form_class(instance=current_change_obj)
            return render(request, 'change.html', {"form": form})
        form = model_form_class(data=request.POST, instance=current_change_obj)
        if form.is_valid():
            self.save(form)
            return redirect(self.reverse_list_url())
        return render(request, 'change.html', {"form": form})

    def list_view(self, request, *args, **kwargs):
        # 批量操作
        action_list = self.get_action_list()
        action_dict = {item.__name__: item.text for item in action_list}
        if request.method == "POST":
            action_name = request.POST.get('action')
            if action_name != '' and action_name in action_dict:
                action_response = getattr(self, action_name)(request, *args, **kwargs)
                if action_response:
                    return action_response
        # 搜索
        search_list = self.get_search_list()
        search_value = request.GET.get('q', '')
        conn = Q()
        conn.connector = "OR"
        if search_value:
            for item in search_list:
                conn.children.append((item, search_value))

        # 排序
        order_list = self.get_order_list()
        query_set = self.model_class.objects.filter(conn).order_by(*order_list)
        all_count = query_set.count()
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
        data_list = query_set[pager.start:pager.end]
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
        # 组合搜索

        search_group = []
        search_columns = self.get_search_group()
        for search_item in search_columns:
            row = search_item.run(self.model_class, request, *args, **kwargs)
            search_group.append(row)

        # 添加按钮
        result = {'header_list': header_list,
                  'body_list': body_list,
                  "current_page_num": current_page_num,
                  'pager': pager,
                  'add_btn': self.get_add_btn(),
                  'search_value': search_value,
                  'search_list': search_list,
                  'action_dict': action_dict,
                  'search_group': search_group
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
