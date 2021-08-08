#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms


class MyBaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MyBaseForm, self).__init__(*args, **kwargs)
        for name, value in self.fields.items():
            value.widget.attrs['class'] = 'form-control'
