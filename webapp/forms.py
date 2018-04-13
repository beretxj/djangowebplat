# -*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelChoiceField
from .models import Node, Line, Device, Market, member, hosts, command


class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        exclude = ['node_signer']


class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        exclude = ['line_signer']


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ['device_signer']


class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        exclude = ['market_signer']


class memberForm(forms.ModelForm):
    class Meta:
        model = member
        exclude = ['member_signer']

'''
class AnsiForm(forms.Form):
    hosts = forms.CharField(max_length=30)
    command = forms.CharField(max_length=30)
'''


class AnsiForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AnsiForm, self).__init__(*args, **kwargs)

    hosts_col = forms.ModelChoiceField(
        queryset = hosts.objects.all(),
        required = True,
        error_messages = {'required': "以下是必填项"},
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'style': 'width:60%',
            }
        ),
    )
    command_col = forms.ModelChoiceField(
        queryset = command.objects.all(),
        required = True,
        error_messages = {'required': "以下是必填项"},
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'style': 'width:60%',
            }
        ),
    )



