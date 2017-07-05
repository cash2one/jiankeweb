# -*- coding:utf-8 -*-

import logging


from django import forms

logger = logging.getLogger('data')


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100, 
            widget=forms.TextInput(attrs={'placeholder': '用户名'}),
            error_messages={'required': '请输入用户名'})
    password = forms.CharField(label='密码', max_length=100, 
            widget=forms.PasswordInput(
                attrs={'placeholder': '密码'}, render_value=False),
            error_messages={'required': '请输入密码'})

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for x in ['username', 'password']:
             self.fields[x].widget.attrs['class'] = 'form-control'

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('用户名和密码为必填项')
        else:
            cleaned_data = super(LoginForm, self).clean()
