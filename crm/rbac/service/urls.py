#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import QueryDict
from django.urls import reverse


def memory_url(request, name, *args, **kwargs):
    url_base = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:
        return url_base
    query_dict = QueryDict(mutable=True)
    query_dict["_filter"] = request.GET.urlencode()
    return f"{url_base}?{query_dict.urlencode()}"


def memory_reverse(request, name, *args, **kwargs):
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get('_filter')
    if origin_params:
        url = f"{url}?{origin_params}"
    return url
