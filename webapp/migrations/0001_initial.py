# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-03 03:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_caption', models.CharField(max_length=100, verbose_name='\u8bbe\u5907\u540d\u79f0')),
                ('device_serial', models.CharField(max_length=100, verbose_name='\u8bbe\u5907\u5e8f\u5217\u53f7')),
                ('device_type', models.CharField(max_length=50, verbose_name='\u8bbe\u5907\u578b\u53f7')),
                ('device_vendor', models.CharField(choices=[('CISCO', 'CISCO'), ('JUNIPER', 'JUNIPER'), ('TOPSEC', 'TOPSEC'), ('HUAWEI', 'HUAWEI'), ('H3C', 'H3C')], max_length=50, verbose_name='\u8bbe\u5907\u5382\u5546')),
                ('device_remark', models.CharField(blank=True, max_length=50, verbose_name='\u5907\u6ce8')),
                ('device_ip', models.GenericIPAddressField(verbose_name='\u7ba1\u7406IP')),
                ('device_status', models.CharField(default='\u542f\u7528', max_length=10, verbose_name='\u8bbe\u5907\u72b6\u6001')),
                ('device_signer', models.CharField(default='system', max_length=30, verbose_name='\u767b\u8bb0\u4eba')),
                ('device_signtime', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_code', models.CharField(max_length=100, verbose_name='\u7ebf\u8def\u7f16\u53f7')),
                ('line_local', models.CharField(default='\u4e0a\u6d77\u6570\u636e\u4e2d\u5fc3', max_length=50, verbose_name='\u6240\u5728\u673a\u623f')),
                ('line_speed', models.CharField(choices=[('2M', '2M'), ('4M', '4M'), ('6M', '6M'), ('10M', '10M'), ('\u5176\u4ed6', '\u5176\u4ed6')], default='6M', max_length=10, verbose_name='\u7ebf\u8def\u901f\u7387')),
                ('line_spname', models.CharField(choices=[('\u4e2d\u56fd\u7535\u4fe1', '\u4e2d\u56fd\u7535\u4fe1'), ('\u4e2d\u56fd\u8054\u901a', '\u4e2d\u56fd\u8054\u901a'), ('\u4e2d\u56fd\u79fb\u52a8', '\u4e2d\u56fd\u79fb\u52a8'), ('\u4e2d\u56fd\u94c1\u901a', '\u4e2d\u56fd\u94c1\u901a'), ('\u5176\u4ed6', '\u5176\u4ed6')], default='\u4fe1\u7f51\u516c\u53f8', max_length=10, verbose_name='\u8fd0\u8425\u5546')),
                ('line_type', models.CharField(choices=[('MSTP', 'MSTP'), ('MSAP', 'MASP'), ('SDH', 'SDH'), ('DIAL', 'DIAL'), ('\u5176\u4ed6', '\u5176\u4ed6')], default='MSTP', max_length=50, verbose_name='\u7ebf\u8def\u7c7b\u578b')),
                ('line_status', models.BooleanField(default=True, verbose_name='\u7ebf\u8def\u542f\u7528')),
                ('line_open', models.DateField(verbose_name='\u5f00\u901a\u65f6\u95f4')),
                ('line_closed', models.DateField(blank=True, null=True, verbose_name='\u5173\u95ed\u65f6\u95f4')),
                ('line_signer', models.CharField(default='system', max_length=30, verbose_name='\u767b\u8bb0\u4eba')),
                ('line_signtime', models.DateField(auto_now_add=True)),
                ('line_remarks', models.CharField(blank=True, max_length=255, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_name', models.CharField(max_length=255, verbose_name='\u5e02\u573a\u540d\u79f0')),
                ('market_address', models.CharField(max_length=255, verbose_name='\u5e02\u573a\u5730\u5740')),
                ('market_contact', models.CharField(blank=True, max_length=255, verbose_name='\u8054\u7cfb\u4eba')),
                ('market_signer', models.CharField(default='system', max_length=50, verbose_name='\u767b\u8bb0\u4eba')),
                ('market_remarks', models.CharField(blank=True, max_length=255, verbose_name='\u5907\u6ce8')),
                ('market_signtime', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_code', models.CharField(max_length=100, verbose_name='\u4f1a\u5458\u7f16\u53f7')),
                ('member_name', models.CharField(max_length=100, verbose_name='\u4f1a\u5458\u540d\u79f0')),
                ('member_local', models.CharField(max_length=100, verbose_name='\u4f1a\u5458\u5730\u5740')),
                ('member_type', models.CharField(choices=[('\u7ecf\u6d4e\u7c7b', '\u7ecf\u6d4e\u7c7b'), ('\u7efc\u5408\u7c7b', '\u7efc\u5408\u7c7b'), ('\u7ed3\u7b97\u7c7b', '\u7ed3\u7b97\u7c7b'), ('\u5176\u4ed6', '\u5176\u4ed6')], default='\u7efc\u5408\u7c7b', max_length=50, verbose_name='\u4f1a\u5458\u7c7b\u578b')),
                ('member_status', models.BooleanField(default=True, verbose_name='\u4f1a\u5458\u72b6\u6001')),
                ('member_open', models.DateField(verbose_name='\u5f00\u901a\u65f6\u95f4')),
                ('member_closed', models.DateField(blank=True, null=True, verbose_name='\u5173\u95ed\u65f6\u95f4')),
                ('member_signer', models.CharField(default='system', max_length=30, verbose_name='\u767b\u8bb0\u4eba')),
                ('member_signtime', models.DateField(auto_now_add=True)),
                ('member_remarks', models.CharField(blank=True, max_length=255, verbose_name='\u5907\u6ce8')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webapp.Market')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_name', models.CharField(max_length=255, verbose_name='\u8282\u70b9\u540d\u79f0')),
                ('node_type', models.CharField(choices=[('\u603b\u90e8', '\u603b\u90e8'), ('\u5206\u90e8', '\u5206\u90e8')], max_length=50, verbose_name='\u8282\u70b9\u7c7b\u578b')),
                ('node_address', models.CharField(max_length=255, verbose_name='\u8282\u70b9\u5730\u5740')),
                ('node_contact', models.CharField(blank=True, max_length=255, verbose_name='\u8282\u70b9\u8054\u7cfb\u4eba')),
                ('node_signer', models.CharField(default='system', max_length=50, verbose_name='\u767b\u8bb0\u4eba')),
                ('node_remarks', models.CharField(blank=True, max_length=255, verbose_name='\u5907\u6ce8')),
                ('node_signtime', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='line',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webapp.Node'),
        ),
        migrations.AddField(
            model_name='device',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webapp.Node'),
        ),
    ]
