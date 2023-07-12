#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: depart.py
@time: 2023/4/23  13:38
"""

from django.core.exceptions import ValidationError
from django.forms import forms
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from user_manage import models
from django.core.paginator import Paginator

def index(request):
    return HttpResponse("Hello, world. This is the user_manage app.")

def depart_list(request):
    """ 部门列表 """

    # 去数据库中获取所有的部门列表
    #  [对象,对象,对象]
    queryset = models.Department.objects.all().order_by('-id')

    # 添加分页功能
    per_page = 10
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    objs = paginator.get_page(page)
    queryset=objs

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 部门添加 """
    if request.method=='GET':
        return render(request, 'depart_add.html')

    # 获取用户通过post请求传来的信息
    title = request.POST.get('title')
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 返回到部门列表 重定向
    # return redirect("/depart/list/")
    return redirect("/depart/add/")


def depart_delete(request):
    """ 删除部门 """
    nid =request.GET.get('nid')
    page=request.GET.get('page')

    # 删除操作
    models.Department.objects.filter(id=nid).delete()

    # 返回到部门列表 重定向
    return redirect(f"/depart/list?page={page}")


def depart_edit(request,nid):# nid 直接从urls中获取
    """ 部门编辑 """

    if request.method == "GET":
        # 根据nid，获取他的数据 [obj,]
        edit_obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"edit_obj": edit_obj})


    # 1.获取用户提交的标题，2.数据库更新，3.重定向返回列表
    depart_title = request.POST.get("depart_title")
    models.Department.objects.filter(id=nid).update(title=depart_title)
    return redirect('/depart/list')


