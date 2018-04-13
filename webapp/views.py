# -*- coding: UTF-8 -*-
import os
import commands
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import NodeForm, LineForm, DeviceForm, MarketForm, memberForm, AnsiForm
from .models import Node, Line, Device, Market, member, hosts, command, T_Host, T_Command
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)

def lists(request, table):
    if table == 'node':
        raw_data = Node.objects.all()
        list_template = 'node_list.html'
        sub_title = '节点信息'
        page_title = '基础信息'
    if table == 'line':
        raw_data = Line.objects.all()
        list_template = 'line_list.html'
        sub_title = '线路信息'
        page_title = '基础信息'
    if table == 'device':
        raw_data = Device.objects.all()
        list_template = 'device_list.html'
        sub_title = '设备信息'
        page_title = '基础信息'
    if table == 'market':
        raw_data = Market.objects.all()
        list_template = 'market_list.html'
        sub_title = '市场信息'
        page_title = '市场管理'
    if table == 'member':
        raw_data = member.objects.all()
        list_template = 'member_list.html'
        sub_title = '会员信息'
        page_title = '市场管理'
    if request.method == 'GET':
        kwargs = {}
        query = ''
        for key, value in request.GET.iteritems():
            if key != 'csrfmiddlewaretoken' and key != 'page':
                #由于线路和设备的外键均与node表格有关，当查询线路中的用户名称或设备信息中的使用部门时，可以直接通过以下方式跨表进行查找
                if key == 'node' or key == 'market':
                    kwargs['node__node_name__contains'] = value
                    #该query用于页面分页跳转时，能附带现有的搜索条件
                    query += '&' + key + '=' + value
                #其余的选项均通过key来辨别
                else:
                    kwargs[key + '__contains'] = value
                    #该query用于页面分页跳转时，能附带现有的搜索条件
                    query += '&' + key + '=' + value
        #通过元始数据进行过滤，过滤条件为健对值的字典
        data = raw_data.filter(**kwargs)
    #如果没有从GET提交中获取信息，那么data则为元始数据
    else:
        data = raw_data
    data_list, page_range, count, page_nums = pagination(request, data)
    context = {
        'data': data_list,
        'table': table,
        'page_title': page_title,
        'sub_title': sub_title,
        'page_range': page_range,
        'count': count,
        'page_nums': page_nums,
        'query': query,
    }
    return render(request,list_template,context)


def add(request, table):
    if table == 'node':
        form = NodeForm(request.POST or None)
        sub_title = '节点信息'
        page_title = '基础信息'
    if table == 'line':
        form = LineForm(request.POST or None)
        sub_title = '线路信息'
        page_title = '基础信息'
    if table == 'device':
        form = DeviceForm(request.POST or None)
        sub_title = '设备信息'
        page_title = '基础信息'
    if table == 'market':
        form = MarketForm(request.POST or None)
        sub_title = '市场信息'
        page_title = '市场管理'
    if table == 'member':
        form = memberForm(request.POST or None)
        sub_title = '会员信息'
        page_title = '市场管理'
    if form.is_valid():
        instance = form.save(commit=False)
        if table == 'node':
            instance.node_signer = request.user
        if table == 'line':
            instance.line_signer = request.user
        if table == 'device':
            instance.device_signer = request.user
        if table == 'market':
            instance.market_signer = request.user
        if table == 'member':
            instance.member_signer = request.user
        instance.save()
        # 跳转至列表页面,配合table参数，进行URL的反向解析
        return redirect('lists', table=table)

        # 创建context来集中处理需要传递到页面的数据
    context = {
        'form': form,
        'table': table,
        'page_title': page_title,
        'sub_title': sub_title,
    }
    return render(request, 'res_add.html', context)


def edit(request, table, pk):
    if table == 'line':
        table_ins = get_object_or_404(Line, pk=pk)
        form = LineForm(request.POST or None, instance=table_ins)
        sub_title = '修改线路信息'
    if table == 'node':
        table_ins = get_object_or_404(Node, pk=pk)
        form = NodeForm(request.POST or None, instance=table_ins)
        sub_title = '修改机构信息'
    if table == 'device':
        table_ins = get_object_or_404(Device, pk=pk)
        form = DeviceForm(request.POST or None, instance=table_ins)
        sub_title = '修改设备信息'
    if table == 'market':
        table_ins = get_object_or_404(Market, pk=pk)
        form = MarketForm(request.POST or None, instance=table_ins)
        sub_title = '修改市场信息'
    if table == 'member':
        table_ins = get_object_or_404(member, pk=pk)
        form = memberForm(request.POST or None, instance=table_ins)
        sub_title = '修改会员信息'
    if form.is_valid():
        # 创建实例，需要做些数据处理，暂不做保存
        instance = form.save(commit=False)
        # 将登录用户作为登记人,在修改时，一定要使用str强制,因为数据库中以charfield方式存放了登记人
        if table == 'node':
            instance.node_signer = str(request.user)
        if table == 'line':
            instance.line_signer = str(request.user)
        if table == 'device':
            instance.device_signer = str(request.user)
        if table == 'market':
            instance.market_signer = str(request.user)
        if table == 'member':
            instance.member_signer = str(request.user)
        instance.save()
        return redirect('lists', table=table)

    context = {
        'table': table,
        'form': form,
        'sub_title': sub_title,
    }
    # 与res_add.html用同一个页面，只是edit会在res_add页面做数据填充
    return render(request, 'res_add.html', context)


def delete(request, table, pk):
    if table == 'line':
        table_ins = get_object_or_404(Line, pk=pk)
    if table == 'node':
        table_ins = get_object_or_404(Node, pk=pk)
    if table == 'device':
        table_ins = get_object_or_404(Device, pk=pk)
    if table == 'market':
        table_ins = get_object_or_404(Market, pk=pk)
    if table == 'member':
        table_ins = get_object_or_404(member, pk=pk)
        # 接收通过AJAX提交过来的POST
    if request.method == 'POST':
        # 删除该条目
        try:
            table_ins.delete()
            data = 'success'
        except IntegrityError:
            data = 'error'
        return JsonResponse(data, safe=False)


def pagination(request, queryset, display_amount=5, after_range_num=3, before_range_num=3):
    # 按参数分页
    try:
        # 从提交来的页面获得page的值
        page = int(request.GET.get("page", 1))
        # 如果page值小于1，那么默认为第一页
        if page < 1:
            page = 1
            # 若报异常，则page为第一页
    except ValueError:
        page = 1
        # 引用Paginator类
    paginator = Paginator(queryset, display_amount)
    # 总计的数据条目
    count = paginator.count
    # 合计页数
    num_pages = paginator.num_pages

    try:
        # 尝试获得分页列表
        objects = paginator.page(page)
        # 如果页数不存在
    except EmptyPage:
        # 获得最后一页
        objects = paginator.page(paginator.num_pages)
        # 如果不是一个整数
    except PageNotAnInteger:
        # 获得第一页
        objects = paginator.page(1)
        # 根据参数配置导航显示范围
    temp_range = paginator.page_range

    # 如果页面很小
    if (page - before_range_num) <= 0:
        # 如果总页面比after_range_num大，那么显示到after_range_num
        if temp_range[-1] > after_range_num:
            page_range = xrange(1, after_range_num + 1)
            # 否则显示当前页
        else:
            page_range = xrange(1, temp_range[-1] + 1)
            # 如果页面比较大
    elif (page + after_range_num) > temp_range[-1]:
        # 显示到最大页
        page_range = xrange(page - before_range_num, temp_range[-1] + 1)
        # 否则在before_range_num和after_range_num之间显示
    else:
        page_range = xrange(page - before_range_num + 1, page + after_range_num)
        # 返回分页相关参数
    return objects, page_range, count, num_pages


def ansible(request):
    if request.method == 'POST':  # 当提交表单时
        form = AnsiForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            hosts_in = form.cleaned_data['hosts_col']
            command_in = form.cleaned_data['command_col']
            os.environ['hosts_in'] = str(hosts_in)
            os.environ['command_in'] = str(command_in)
            outputstr = commands.getoutput("sh /ansi/$command_in $hosts_in")
            output = []
            output = outputstr.split("\n")
            context = {
                'output': output,
            }
            return render(request, 'ansi-result.html', context)
    else:  # 当正常访问时
        form = AnsiForm()
    return render(request, 'ansible.html', {'form': form})


def ansiget(request):
    template = get_template('ansiget.html')
    hostsdata = T_Host.objects.all()
    commanddata = T_Command.objects.all()
    try:
        hosts_get = request.GET['host_id']
        command_get = request.GET['command_id']
        os.environ['hosts_get'] = str(hosts_get)
        os.environ['command_get'] = str(command_get)
        outputstr = commands.getoutput("sh /ansi/$command_get $hosts_get")
        #output = []
        #output = outputstr.split("\n")
        html = template.render(locals())
        return HttpResponse(html)
    except:  # 当正常访问时
        html = template.render(locals())
    return HttpResponse(html)