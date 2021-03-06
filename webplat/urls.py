"""webplat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import webapp.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', webapp.views.index),
    url(r'^ansible/', webapp.views.ansible),
    url(r'^ansiget/', webapp.views.ansiget),
    url(r'^index/', webapp.views.index, name='index'),
    url(r'^lists/(?P<table>\w+)/$', webapp.views.lists, name='lists'),
    url(r'^add/(?P<table>\w+)/$', webapp.views.add, name='add'),
    url(r'^edit/(?P<table>\w+)/(?P<pk>\d+)/$', webapp.views.edit, name='edit'),
    url(r'^delete/(?P<table>\w+)/(?P<pk>\d+)/$', webapp.views.delete, name='delete'),
    url(r'^task_list/', webapp.views.task_list, name='task_list'),
    url(r'^task_add/', webapp.views.task_add, name='task_add'),
    url(r'^task_edit/(?P<pk>\d+)/$', webapp.views.task_edit, name='task_edit'),
    url(r'^task_delete/(?P<pk>\d+)/$', webapp.views.task_delete, name='task_delete'),
    url(r'^upload_file/(?P<pk>\d+)/$', webapp.views.upload_file, name='upload_file'),
    url(r'^task_finish/(?P<pk>\d+)/$', webapp.views.task_finish, name='task_finish'),
    url(r'^process_edit/(?P<pk>\d+)/$', webapp.views.process_edit, name='process_edit'),
    url(r'^process_delete/(?P<pk>\d+)/$',webapp.views.process_delete, name='process_delete'),
    url(r'login/', webapp.views.login, name='login'),
    url(r'logout/', webapp.views.logout, name='logout'),
    url(r'password_change/', webapp.views.password_change, name='password_change'),
    url(r'^editor/', include('editor.urls', namespace='editor', app_name='editor')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
