#coding:utf-8
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from editor import models
from editor import object2word
from docx import Document
from .forms import projectForm, bugForm, SelectTestFrom
from django.views.decorators.csrf import csrf_exempt ,csrf_protect
import json
import os
import random
import time
import sys
from webplat import settings
base = settings.BASE_DIR
print base
#装饰器@csrf_exempt表示不用CSRF防护,@csrf_protect需要防护
# Create your views here.

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

wordDir = os.path.join(base,'static','word')
imgDIR = os.path.join(base,'static','upload','img')
BASE_URI = 'http://127.0.0.1:8000/'
fileType = ['png','jpg']


def get_content(req):
    if req.method == 'POST':
        content = req.POST['content']
        print
        content + "----------------------------------"
        return render(req, 'e_projects_view.html', {'article_id': content})
    else:
        return render(req, 'e_projects_view.html', {})


# 处理编辑器图片上传
@csrf_exempt
def uploadEditor(req):
    funcNum = req.GET['CKEditorFuncNum']
    if req.method == 'POST':
        if req.FILES:
            obj = req.FILES['upload']
            if obj.name.strip().split('.')[-1] in fileType:
                filename = str(random.random()) + '_' + obj.name
                date = time.strftime('%Y%m%d', time.localtime(time.time()))
                uppath = os.path.join(imgDIR, date)
                if not os.path.exists(uppath):
                    os.mkdir(uppath)
                filepath = os.path.join(uppath, filename)
                fileurl = BASE_URI + 'static/upload/img/' + date + '/' + filename
                with open(filepath, 'wb') as destination:
                    for chunk in obj.chunks():
                        destination.write(chunk)
                # 将图片url返回给编辑器
                return HttpResponse(
                    "<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction(" + funcNum + ", '" + fileurl + "', '上传成功');</script>")
            else:
                return HttpResponse(
                    "<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction(" + funcNum + ", '请上传jpg/png图片', '请上传jpg/png图片');</script>")


# 处理编辑器复制上传图片
@csrf_exempt
def uploadPaste(req):
    if req.method == 'POST':
        if req.FILES:
            obj = req.FILES['upload']
            if obj.name.strip().split('.')[-1] in fileType:
                filename = str(random.random()) + '_' + obj.name
                date = time.strftime('%Y%m%d', time.localtime(time.time()))
                uppath = os.path.join(imgDIR, date)
                if not os.path.exists(uppath):
                    os.mkdir(uppath)
                filepath = os.path.join(uppath, filename)
                fileurl = BASE_URI + 'static/upload/img/' + date + '/' + filename
                with open(filepath, 'wb') as destination:
                    for chunk in obj.chunks():
                        destination.write(chunk)
                # 返回json数据给编辑器
                info1 = {}
                info1['message'] = 'errorMsg'
                info = {}

                info['uploaded'] = 1
                info['fileName'] = obj.name
                info['url'] = fileurl
                info['error'] = info1
                jsonResult = json.dumps(info)
                # 将图片url返回给编辑器
                return HttpResponse(jsonResult)


def index(req):
    articles = models.Article.objects.all()
    return render(req, 'e_index.html', {'articles': articles})


def article_page(req, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(req, 'e_article_page.html', {'article': article})


def work(req):
    projects = models.Project.objects.order_by("p_time")
    return render(req, 'e_work.html', {'projects': projects})


def project_view(req, project_id):
    project = models.Project.objects.get(pk=project_id)
    bugs = project.bug_set.all()
    form = SelectTestFrom()
    return render(req, 'e_project_view.html', {'bugs': bugs, 'project': project, 'form': form})


def project_del(req, project_id):
    project = models.Project.objects.get(pk=project_id)
    project.delete()
    return HttpResponseRedirect('/editor/work/')


@csrf_exempt
def project_add(req):
    if req.method == 'POST':
        form = projectForm(req.POST)
        if form.is_valid():
            p_name = form.cleaned_data['p_name']
            p_time = form.cleaned_data['p_time']
            p_charge = form.cleaned_data['p_charge']
            models.Project.objects.create(p_name=p_name, p_time=p_time, p_charge=p_charge)
            return HttpResponseRedirect('/editor/work/', 'ok!')
    else:
        form = projectForm()
    return render(req, 'e_project_add.html', {'form': form})


def bug_view(req, bug_id):
    bug = models.Bug.objects.get(pk=bug_id)
    project = bug.b_project
    if req.method == 'POST':
        bug.b_name = req.POST.get('b_name', 1)
        bug.b_risk = req.POST.get('b_risk', 1)
        bug.b_level = req.POST.get('b_level', 1)
        bug.b_details = req.POST.get('content', 1)
        bug.b_repair = req.POST.get('b_repair', 1)
        bug.b_url = req.POST.get('b_url', 1)
        bug.save()
        return HttpResponseRedirect('/editor/project_view/' + str(project.id))
    return render(req, 'e_bug_view.html', {'bug': bug, 'project': project})


def bug_del(req, bug_id):
    bug = models.Bug.objects.get(pk=bug_id)
    bug.delete()
    project_id = str(bug.b_project_id)
    return HttpResponseRedirect('/editor/project_view/' + project_id)

@csrf_exempt
def bug_add(req, project_id):
    select = req.POST.get('bug')
    project = models.Project.objects.get(pk=project_id)
    if req.method == 'POST' and select == None:
        b_name = req.POST.get('b_name', 1)
        b_risk = req.POST.get('b_risk', None)
        b_level = req.POST.get('b_level', 1)
        b_details = req.POST.get('content', 1)
        b_repair = req.POST.get('b_repair', None)
        b_url = req.POST.get('b_url', 1)
        models.Bug.objects.create(b_name=b_name, b_risk=b_risk, b_level=b_level, b_details=b_details, b_repair=b_repair,
                                  b_url=b_url, b_project=project)
        return HttpResponseRedirect('/editor/project_view/' + project_id)
    try:
        bug = models.BugModel.objects.all().get(b_name=select)
    except:
        return render(req, 'e_bug_add.html', {'project': project})
        print
        '------------------------------------'
    return render(req, 'e_bug_add.html', {'bug': bug, 'project': project})


def project_word(req, project_id):
    project = models.Project.objects.get(pk=project_id)
    document = Document()
    doc = object2word.Object2word(document)
    filename = project.p_name + '_' + project.p_time + '.docx'
    filedir = os.path.join(wordDir, filename).encode('gbk')
    doc.handleproject(project).save(filedir)
    return HttpResponseRedirect('/static/word/' + filename)


def select(req):
    form = SelectTestFrom()
    if req.method == 'POST':
        bb = req.POST.get('bug')
        try:
            bug = models.BugModel.objects.all().get(b_name=bb)
        except:
            return render_to_response('e_select.html', {'form': form})

        return render(req, 'e_select.html', {'form': form, 'bb': bb, 'bug': bug})
    return render(req, 'e_select.html', {'form': form})


