#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: admin.py
@time: 2023/4/23  15:29
"""
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404

from user_manage.utils import pagination
from user_manage import models
from user_manage.models import Admin

from user_manage.utils.bootstrap import BootStrapModelForm
from user_manage.utils.encrypt import md5

def admin_list(request):
    '''管理员列表'''

    '''来源是account登录操作传送info到数据库 获取session中的info值 
        也可以直接再html中调用
    '''
    # print(request.session['info'])

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_obj=pagination.Pagination
    page_object = page_obj(request, queryset,page_size=5)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
    }
    return render(request, 'admin_list.html', context)

class Admin_add_ModelForm(BootStrapModelForm):

    # 在modelform中添加新字段 常用于确认事件
    confirm_password=forms.CharField(
        label='确认密码',
        # 脱敏操作  # render_value=False报错时不清除数据
        widget=forms.PasswordInput(render_value=False)
    )

    class Meta:
        model = models.Admin
        fields =['name','password','confirm_password']
        # widgets={
            # 'password':forms.PasswordInput(render_value=True) #报错时不清除数据
        # }

    # 密码进行MD5加密
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    # 校验密码是否一直
    def clean_confirm_password(self):
        print(self.cleaned_data) #{'name': 'carlos', 'password': '2ac77fdb13b12f63aabc6658b3834032', 'confirm_password': '22211'}

        pwd=self.cleaned_data.get('password')
        confirm_pwd=md5(self.cleaned_data.get('confirm_password'))# 对确认密码MD5加密，保证前端传入值为密文

        if confirm_pwd!=pwd:
            raise ValidationError(f'两次输入的密码不一致\n请重新输入')

        # return 什么 次字段返回数据库值就会是什么
        return confirm_pwd

class Admin_edit_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields =['name']
        widgets={
            # 'password':forms.PasswordInput(render_value=True) #报错时不清除数据
        }

def admin_add(request):
    '''添加管理员'''

    html_title='新建管理员'
    if   request.method == "GET":
        model_forms=Admin_add_ModelForm

        return render(request,'change.html',{'form':model_forms,'title':html_title})

    model_forms = Admin_add_ModelForm(data=request.POST)
    if model_forms.is_valid():

        model_forms.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': model_forms, "title": html_title})


def admin_edit(request,nid):
    '''编辑管理员'''

    # 对象 /None 先判断是否有对应的数据
    input_obj=models.Admin.objects.filter(id=nid).first()
    if not input_obj:
        return render(request,'error.html',{"msg":"没有找到对应的用户"})

    html_title = '编辑管理员'
    if   request.method == "GET":
        model_forms=Admin_edit_ModelForm(instance=input_obj)# 默认值
        return render(request,'change.html',{'form':model_forms,'title':html_title})

    model_forms =Admin_edit_ModelForm(data=request.POST,instance=input_obj)
    if model_forms.is_valid():

        model_forms.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': model_forms, "title": '傻逼为什么姓名都不填'})

def admin_delete(request,nid):

    # 对象 /None 先判断是否有对应的数据
    input_obj = models.Admin.objects.filter(id=nid).first()
    if not input_obj:
        return render(request, 'error.html', {"msg": "没有找到对应的用户"})

    admin = get_object_or_404(Admin, id=nid)
    admin.delete()

    # 返回到管理员列表 重定向
    return redirect(f"/admin/list")

def admin_reset(request,nid):
    # 对象 /None 先判断是否有对应的数据
    input_obj = models.Admin.objects.filter(id=nid).first()
    if not input_obj:
        return render(request, 'error.html', {"msg": "没有找到对应的用户"})

    # 重置密码为123456，并进行md5加密
    input_obj.password=md5('123456')
    print('加密后',input_obj.password)
    input_obj.save()

    # 返回到管理员列表 重定向
    return redirect(f"/admin/list")


