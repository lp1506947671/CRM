#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render


class StarkHandler:
    def __init__(self, model_class, prev):
        self.model_class = model_class
        self.prev = prev

    def add_view(self, request):
        return HttpResponse("增加")

    def delete_view(self, request, pk):
        return HttpResponse("删除")

    def change_view(self, request, pk):
        return HttpResponse("改变")

    def list_view(self, request):
        data_list = self.model_class.objects.all()
        return render(request, 'changelist.html', {'data_list': data_list})

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
            url(r"^change/(\d+)$", self.delete_view, name=self.url_name("change")),
            url(r"^del/$", self.change_view, name=self.url_name("list")),
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
