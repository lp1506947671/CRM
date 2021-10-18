"""
分页组件
"""
from django import template

# 创建注册对象
register = template.Library()


@register.inclusion_tag("pagination.html", takes_context=True)
def my_paginator(context):
    dict1 = {
        "has_previous": context["has_previous"],
        "previous_page_number": context["previous_page_number"],
        'has_next': context["has_next"],
        'next_page_number': context["next_page_number"],
        'page_range': context["page_range"],
    }
    return dict1
