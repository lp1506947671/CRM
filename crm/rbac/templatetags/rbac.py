#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag('../templates/menu.html')
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    return {
        'menu_list': menu_list
    }
