#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from collections import OrderedDict

from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag('../templates/menu.html')
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    for item in menu_list:
        regex = f"^{item['url']}$"
        if re.match(regex, request.path_info):
            item['class'] = 'active'
    return {
        'menu_list': menu_list
    }


@register.inclusion_tag('../templates/multi_menu.html')
def multi_menu(request):
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    if not menu_dict:
        return
    key_list = sorted(menu_dict)
    ordered_dict = OrderedDict()

    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for per in val['children']:
            regex = f'^{per["url"]}$'
            if re.match(regex, request.path_info):
                per['class'] = 'active'
                val['class'] = ''
            ordered_dict[key] = val
    return {'menu_dict': ordered_dict}
