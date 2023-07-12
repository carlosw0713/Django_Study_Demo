#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: user.py
@time: 2023/4/23  13:38
"""

from django.core.exceptions import ValidationError
from django.forms import forms
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from user_manage import models
from user_manage.models import UserInfo,Department
from django.core.paginator import Paginator
from user_manage.utils.form import UserModelForm_add,UserModelForm_edit

def user_list(request):
    """ 用户管理 """

    # 获取所有用户列表 [obj,obj,obj]
    queryset = models.UserInfo.objects.all()

    # 搜索框
    data_dict = {}
    search_data = request.GET.get('name', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.UserInfo.objects.filter(**data_dict)



    # 添加分页功能
    per_page = 5
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    # 用Python的语法获取数据
    # for obj in queryset:

        # obj.depart_id  # 获取数据库中存储的那个字段值
        # 数据库索引 在创建数据库时规定的 在models模块中配置
        # obj.depart.title  # 根据id自动去关联的表中获取哪一行数据depart对象。

        # print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
        # try:
        #     print(obj.name, obj.dapart.title)
        # except:
        #     pass

    return render(request, 'user_list.html', {"queryset": queryset})

def user_add(request):
    """ 添加用户（原始方式） """

    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }

        # 添加分页功能


        return render(request, 'user_add.html', context)

    '''原始提交方式
    1.用户提交得有数据校验
    2.用户没有提交没有错误提示
    3.页面上，每个字段都需要我们重新写一遍
    4.关联的数据，手动去获取并展示在页面'''
    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list/")




def user_model_form_add(request):
    '''添加用户（ModelForm版本）'''

    if request.method == "GET":
        form = UserModelForm_add()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户提交数据，数据验证。
    form_post = UserModelForm_add(data=request.POST)
    # 判断数据类型是否合法
    if form_post.is_valid():
        # 通过form.instance.字段名 =值 进行而外的添加 常用于获取当前时间
        form_post.instance.password = 123456

        # 直接将表单返回所有信息提交到数据库
        form_post.save()
        return  redirect('user_list_redirect')

    # 校验失败 （在当前页面显示错误信息  错误信息是由填写完表单后返回的）
    return render(request, 'user_model_form_add.html', {"form": form_post})





def user_edit(request,nid):# nid 直接从urls中获取
    """ 用户编辑 """

    # 从数据库中获取该用户对象
    user = get_object_or_404(UserInfo, id=nid)
    if request.method == "POST":
        # 如果请求方法是 POST，则处理提交的表单数据
        form = UserModelForm_edit(data=request.POST, instance=user)
       


        


        if form.is_valid():
            
            # 调用钩子函数校验pasword
            form.password=form.password_6()
            print(form.cleaned_data)

            form.save()
            '''
            return redirect('user_list') 和 return redirect('user/list') 之间的区别在于 URL 配置中的名称。
            Django 中的 redirect() 函数需要接受 URL 名称或 URL 路径作为参数，因此如果您未正确指定 URL 配置中使用的名称，则可能会出现问题。
            因此最好直接定义跳转的路径名称path('user/list/', views.user_list,name='user_list_redirect'),
            '''
            return redirect('user_list_redirect')
    else:
        # 如果请求方法是 GET，则创建一个新表单并将其预先填充到用户数据中
        form = UserModelForm_edit(instance=user)
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request):
    """ 删除部门 """
    '''
    通常情况下，我们不需要使用 ModelForm 来执行删除操作，因为删除操作涉及的是数据库的删除操作
    ，而不是表单数据的提交。因此，我们可以直接使用 Django 模型管理器中的 delete() 方法来执行
    删除操作。以下是一个示例视图函数，演示如何使用 Django 模型管理器执行删除操作：
    '''

    nid =request.GET.get('nid')
    page=request.GET.get('page')

    # 删除操作 传统操作
    # models.UserInfo.objects.filter(id=nid).delete()

    user = get_object_or_404(UserInfo, id=nid)
    user.delete()

    # 返回到部门列表 重定向
    return redirect(f"/user/list?page={page}")
