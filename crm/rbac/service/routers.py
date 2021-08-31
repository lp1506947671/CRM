#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from collections import OrderedDict

from django.urls import URLPattern, URLResolver
from django.utils.module_loading import import_string

from crm import settings


def check_url_exclude(url):
    """排除一些特定的url"""
    # url正则在settings.中则排除
    return any([True for item in settings.AUTO_DISCOVER_EXCLUDE if re.match(item, url)])


def recursion_url(pre_namespace, pre_url: str, urlpatterns, result: dict):
    """
    pre_namespace: namespace前缀,以后用户拼接name
    pre_url: url前缀,用于拼接url
    urlpatterns: 路由关系列表
    result: 用于保存递归中获取的所有的路由
    """
    # 遍历urlpatterns
    for item in urlpatterns:
        if isinstance(item, URLPattern):
            # 非路由分发,添加到result
            if not item.name:
                # 别名name不存在直接跳过
                continue
            # 拼接namespace:name(namespace存在和不存在的两种情况)
            name = f"{pre_namespace}:{item.name}" if pre_namespace else item.name
            # 拼接url(去除^和$)
            url = pre_url + str(item.pattern)
            url = url.replace("^", "").replace("$", "")
            if check_url_exclude(url):
                # 如果是exclude中的url则直接跳过
                continue
            # 否者追加到result中
            result[name] = {"name": name, "url": url}
        if isinstance(item, URLResolver):
            # 路由分发 递归操作
            if pre_namespace:
                # namespace前缀存在
                # namespace存在与否
                namespace = f"{pre_namespace}:{item.namespace}" if item.namespace else pre_namespace
            else:
                # namespace前缀不存在
                # namespace存在与否
                namespace = item.namespace if item.namespace else None
            url = pre_url + str(item.pattern)
            recursion_url(namespace, url, item.url_patterns, result)


def get_all_url_dict():
    """获取项目中所有的url(必须有那么别名)"""
    # 创建有序字典OrderedDict
    url_order_dict = OrderedDict()
    # 导入setting.ROOT_URLCONF
    md = import_string(settings.ROOT_URLCONF)
    recursion_url(None, "/", md.urlpatterns, url_order_dict)
    # 递归获取所有的路由
    return url_order_dict
