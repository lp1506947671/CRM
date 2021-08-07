#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from rbac import models


class UserModelForm(forms.ModelForm):
    """
    1.model字段,新增字段
    2.添加form-control
    3.检查密码是否一致
    """
    rest_password = forms.CharField(label="确认密码")

    class Meta:
        model = models.UserInfo
        fields = ["name", "email", 'password', "rest_password"]

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, value in self.fields.items():
            value.widget.attrs['class'] = 'form-control'

    def clean_rest_password(self):
        password = self.changed_data['password']
        rest_password = self.changed_data['rest_password']
        if password != rest_password:
            raise ValidationError("两次输入密码不一致")
        return rest_password


class UpdateUserModelForm(forms.ModelForm):
    """
    1.model字段,新增字段
    2.添加form-control
    """

    class Meta:
        model = models.UserInfo
        fields = ["name", "email"]

    def __init__(self, *args, **kwargs):
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        for name, value in self.fields.items():
            value.widget.attrs['class'] = 'form-control'


class ResetPasswordUserModelForm(forms.ModelForm):
    """
     1.model字段,新增字段
    2.添加form-control
    """
    rest_password = forms.CharField(label="确认密码")

    class Meta:
        model = models.UserInfo
        fields = ['password', "rest_password"]

    def __init__(self, *args, **kwargs):
        super(ResetPasswordUserModelForm, self).__init__(*args, **kwargs)
        for name, value in self.fields.items():
            value.widget.attrs['class'] = 'form-control'

    def clean_rest_password(self):
        """
        检测密码是否一致
        :return:
        """
        password = self.cleaned_data['password']
        rest_password = self.cleaned_data['rest_password']
        if password != rest_password:
            raise ValidationError('两次密码输入不一致')
        return rest_password
