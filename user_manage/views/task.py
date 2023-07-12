#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: task.py
@time: 2023/4/25  14:03
"""
import json

from django import forms
from user_manage import models

from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from user_manage.utils.bootstrap import BootStrapModelForm

from user_manage.utils.pagination import Pagination
class TaskModelForm(BootStrapModelForm):

    # 我们重写了表单类的 __init__ 方法，并并为 user_id 和 detail 字段分别指定了默认值
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 通过 initial 指定 user_id 的默认值
        initial = {
            'user_id': 1,
            'detail': '不知道要填写些什么111',
        }
        self.initial.update(initial)


    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput,
            # "user_id": forms.Select(),

        }



def task_list(request):
    '''任务列表'''

    queryset=models.Task.objects.all().order_by('-id')

    form=TaskModelForm() #获取 添加表单信息

    # 分页
    page_object = Pagination(request, queryset,page_size=3)
    context={
        'form':form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
    }
    # print(page_object.html())


    return render(request,'task_list.html',context)


@csrf_exempt
def task_ajax(request):
    '''ajax信息接收发送'''

    # 获取ajax传来的data信息
    if request.GET:
        data=request.GET

    data=request.POST

    print(request.GET)
    print(request.POST)

    data_dict = {"status": True, 'data': data}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    # {'level': ['1'], 'title': ['sdfsdfsdfsd'], 'detail': ['111'], 'user': ['8']}
    # print(request.POST)

    # 1.用户发送过来的数据进行校验（ModelForm进行校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
