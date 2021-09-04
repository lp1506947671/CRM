#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms

from django.utils.safestring import mark_safe

from rbac import models

ICON_LIST = [
    ['fa-hand-scissors-o', '<i aria-hidden="true" class="fa fa-hand-scissors-o"></i>'],
    ['fa-hand-spock-o', '<i aria-hidden="true" class="fa fa-hand-spock-o"></i>'],
    ['fa-hand-stop-o', '<i aria-hidden="true" class="fa fa-hand-stop-o"></i>'],
    ['fa-handshake-o', '<i aria-hidden="true" class="fa fa-handshake-o"></i>'],
    ['fa-hard-of-hearing', '<i aria-hidden="true" class="fa fa-hard-of-hearing"></i>'],
    ['fa-hashtag', '<i aria-hidden="true" class="fa fa-hashtag"></i>'],
    ['fa-hdd-o', '<i aria-hidden="true" class="fa fa-hdd-o"></i>'],
    ['fa-headphones', '<i aria-hidden="true" class="fa fa-headphones"></i>'],
    ['fa-heart', '<i aria-hidden="true" class="fa fa-heart"></i>'],
    ['fa-heart-o', '<i aria-hidden="true" class="fa fa-heart-o"></i>'],
    ['fa-heartbeat', '<i aria-hidden="true" class="fa fa-heartbeat"></i>'],
    ['fa-history', '<i aria-hidden="true" class="fa fa-history"></i>'],
    ['fa-home', '<i aria-hidden="true" class="fa fa-home"></i>'],
    ['fa-hotel', '<i aria-hidden="true" class="fa fa-hotel"></i>'],
    ['fa-hourglass', '<i aria-hidden="true" class="fa fa-hourglass"></i>'],
    ['fa-hourglass-1', '<i aria-hidden="true" class="fa fa-hourglass-1"></i>'],
    ['fa-hourglass-2', '<i aria-hidden="true" class="fa fa-hourglass-2"></i>'],
    ['fa-hourglass-3', '<i aria-hidden="true" class="fa fa-hourglass-3"></i>'],
    ['fa-hourglass-end', '<i aria-hidden="true" class="fa fa-hourglass-end"></i>'],
    ['fa-hourglass-half', '<i aria-hidden="true" class="fa fa-hourglass-half"></i>'],
    ['fa-hourglass-o', '<i aria-hidden="true" class="fa fa-hourglass-o"></i>'],
    ['fa-hourglass-start', '<i aria-hidden="true" class="fa fa-hourglass-start"></i>'],
    ['fa-i-cursor', '<i aria-hidden="true" class="fa fa-i-cursor"></i>'],
    ['fa-id-badge', '<i aria-hidden="true" class="fa fa-id-badge"></i>'],
    ['fa-id-card', '<i aria-hidden="true" class="fa fa-id-card"></i>'],
    ['fa-id-card-o', '<i aria-hidden="true" class="fa fa-id-card-o"></i>'],
    ['fa-image', '<i aria-hidden="true" class="fa fa-image"></i>'],
    ['fa-mail-reply-all', '<i aria-hidden="true" class="fa fa-mail-reply-all"></i>'],
    ['fa-reply', '<i aria-hidden="true" class="fa fa-reply"></i>'],
    ['fa-reply-all', '<i aria-hidden="true" class="fa fa-reply-all"></i>'],
    ['fa-retweet', '<i aria-hidden="true" class="fa fa-retweet"></i>'],
    ['fa-wrench', '<i aria-hidden="true" class="fa fa-wrench"></i>']]
ICON_LIST = [[item[0], mark_safe(item[1])] for item in ICON_LIST]


class MyBaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MyBaseForm, self).__init__(*args, **kwargs)
        for name, value in self.fields.items():
            value.widget.attrs['class'] = 'form-control'


class MenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ['title', "icon"]
        widgets = {
            'title': forms.TextInput(attrs={"class": 'form-control'}),
            'icon': forms.RadioSelect(choices=ICON_LIST, attrs={'class': 'clearfix'})
        }


class SecondMenuForm(MyBaseForm):
    class Meta:
        model = models.Permission
        exclude = ['pid']


class PermissionMenuForm(MyBaseForm):
    class Meta:
        model = models.Permission
        fields = ['title', "name", "url"]


class MultiAddPermission(MyBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Permission
        exclude = ['id']


class MultiEditPermission(MyBaseForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')] + list(models.Menu.objects.values_list('id', 'title')),
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,

    )

    pid_id = forms.ChoiceField(
        choices=[(None, '-----')] + list(
            models.Permission.objects.filter(pid__isnull=True).exclude(menu__isnull=True).values_list('id', 'title')),
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Permission
        fields = ['id', 'title', "url", "name", "menu_id", "pid_id"]


# class MultiEditPermission(forms.Form):
#     id = forms.IntegerField(
#         widget=forms.HiddenInput()
#     )
#
#     title = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     url = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     name = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     menu_id = forms.ChoiceField(
#         choices=[(None, '-----')],
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#
#     )
#
#     pid_id = forms.ChoiceField(
#         choices=[(None, '-----')],
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#
#
# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
#     self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
#         menu__isnull=True).values_list('id', 'title')
