# -*- coding: UTF-8 -*-
from django import forms

class projectForm(forms.Form):
    p_name = forms.CharField()
    p_time = forms.CharField()
    p_charge = forms.CharField()


class bugForm(forms.Form):
    b_name = forms.CharField()
    b_risk = forms.CharField()
    b_level = forms.CharField()
    b_repair = forms.CharField()
    b_url = forms.CharField()


class SelectTestFrom(forms.Form):
    bug = forms.CharField(
        widget=forms.Select(
            choices=(
                ('null', 'null'),
                ('跨站脚本漏洞','XSS'),
                ('越权漏洞','越权漏洞'),
                ('sql','SQL注入'),
            ),
            attrs={"class": "form-control"}
        ),
        required=True
    )