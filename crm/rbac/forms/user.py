#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms


class UserModelForm(forms.ModelForm):
    """
    1.model字段,新增字段
    2.添加form-control
    3.检查密码是否一致
    """

    ...


class UpdateUserModelForm(forms.ModelForm):
    """
    1.model字段,新增字段
    2.添加form-control
    """
    ...


class ResetPasswordUserModelForm(forms.ModelForm):
    """
     1.model字段,新增字段
    2.添加form-control
    """
