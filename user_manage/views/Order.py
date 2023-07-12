#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: Order.py
@time: 2023/4/26  16:13
"""
import random
from datetime import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from user_manage import models
from user_manage.utils.bootstrap import BootStrapModelForm
from user_manage.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):

    class Meta:
        model=models.Order
        # fields='__all__'
        exclude = ('oid','username')   # exclude = ["oid"]  两种方式 不显示oid

def Order_list(request):

    queryset=models.Order.objects.all().order_by('-id')
    form=OrderModelForm() #获取 添加表单信息

    # 分页
    page_object = Pagination(request, queryset,page_size=5)
    context={
        'form':form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
    }
    # print(context)


    return render(request,'Order_list.html',context)


# post请求一定要传csrf 验证
@csrf_exempt
def Order_add(request):

    form = OrderModelForm(data=request.POST)
    '''form.is_valid()用于验证表单数据是否合法，如果数据合法则返回 True，否则返回 False。'''
    if form.is_valid():

        form.instance.oid=datetime.now().strftime("%Y-%m-%d-%H%M")+"$"+str(random.randint(100,999))
        # 从session中取当前用户id
        form.instance.username_id=request.session["info"].get('id')

        form.save()
        data_dict = {"status": True}

        #等价
        # return HttpResponse(json.dumps(data_dict))
        return JsonResponse(data_dict)



    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


def Order_delete(request):
    '''删除订单'''

    uid=request.GET.get('uid')
    # uid=1111
    print(uid)
    # 判断是否存在
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status":False ,"error":"数据不存在,删除失败."})
    
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status':True})


def Order_detail(request):
    '''更具id获取编辑对象'''
    uid=request.GET.get('uid')
    print(uid)

    '''第一种方式通过返回的数据对象一个个获取所需要的字段信息'''
    # row_object= models.Order.objects.filter(id=uid).first()
    # if not row_object:
    #     return JsonResponse({'status':False,'message':'订单ID不存在'})
    
    # result={
    #     'status':True,
    #     "data":{
    #     'title':row_object.title,
    #     'price':row_object.price,
    #     'status':row_object.status
    #     }
    # }

    '''第二种方法,直接获取对象返回的json格式数据'''
    row_object= models.Order.objects.filter(id=uid).values('title','price','status').first()
    if not row_object:
        return JsonResponse({'status':False,'message':'订单ID不存在'})
    
    result={
        'status':True,
        "data":row_object
    }

    return JsonResponse(result)

# post请求一定要传csrf 验证
@csrf_exempt
def Order_edit(request):

    uid=request.GET.get('uid')
    row_object= models.Order.objects.filter(id=uid).first()
    print(row_object)
    '''form.is_valid()用于验证表单数据是否合法，如果数据合法则返回 True，否则返回 False。'''

    if not row_object:
        return JsonResponse({'status':False,'edit_messages':'订单ID不存在'})


    form=OrderModelForm(data=request.POST,instance=row_object)
    if form.is_valid():

        # row_object.instance.oid=datetime.now().strftime("%Y-%m-%d-%H%M")+"$"+str(random.randint(100,999))

        # # 从session中取当前用户id
        # row_object.instance.username_id=request.session["info"].get('id')

        form.save()
        data_dict = {"status": True}

        #等价
        # return HttpResponse(json.dumps(data_dict))
        return JsonResponse(data_dict)

  
    #  如果 返回的值不满足校验 is_valid 返回错误信息
    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))