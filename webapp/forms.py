# -*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelChoiceField
from .models import Node, Line, Device, Market, member, hosts, command, Employee


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


class TaskForm(forms.Form):
    #任务类型的分类
    category = (
        (U'综合事务','综合事务'),
        (U'机构建设','机构建设'),
        (U'线路事务','线路事务'),
    )
    task_title = forms.CharField(label = '任务名称',max_length = 255)
    task_category = forms.ChoiceField(label='任务分类',choices= category)
    #建立联系人，其中的textarea做了规格设定，默认行高为2
    task_contacts = forms.CharField(label = '联系人',widget=forms.Textarea(attrs={'rows': '2'}),required=False)
    #建立一个复选框的实施人员，通过queryset来获取人员列表
    task_member = forms.ModelMultipleChoiceField(label='实施人员',
                                                 queryset=Employee.objects.all(),
                                                 widget=forms.CheckboxSelectMultiple)
    #建立一个处理过程
    process_content = forms.CharField(label = '处理过程',widget=forms.Textarea)


class UploadFileForm(forms.Form):
    #提供一个上传附件的FORM
    file = forms.FileField() 

#建立实施步骤的表单
class ProcessForm(forms.Form):
    process_content = forms.CharField(label = '处理过程',widget=forms.Textarea)

