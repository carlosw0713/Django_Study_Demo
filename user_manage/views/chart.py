#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: chart.py
@time: 2023/5/5  14:01
"""

from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from user_manage import models

def chart_list(request):

    return render(request,'chart.html')


def chart_bar(request):


    legend= ['销量','业绩']
    x_axis= ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    series_list= [
            {
              'name': '销量',
              'type': 'bar',
              'data': [5, 20, 36, 10, 10, 20]
            },
            {
              'name': '业绩',
              'type': 'bar',
              'data': [50, 6, 33, 100, 10, 25]
            }
          ]
       
    result={
        'status':True,
        'data':{
            'legend':legend,
            'x_axis':x_axis,
            'series_list':series_list,
        }
    }

    # print(result)

    return JsonResponse(result)


def chart_pie(request):

    # series_list=[
    #     { 'value': 1048, 'name': '人事部' },
    #     { 'value': 735, 'name': '研发部' },
    #     { 'value': 580, 'name': '外贸部' },
    #     { 'value': 484, 'name': '保安部' },
    #     { 'value': 300, 'name': 'CBO' }
    #   ]

    # 获取数据库的值 赋值到饼图上
    data=models.performance.objects.all()
    series_list=[]
    for obj in data:
        dict={ 'value': obj.sales ,'name': obj.depart }
        series_list.append(dict)

        # print(obj.sales,obj.depart)


    result={
    'status':True,
    'data':{
        'series_list':series_list,
    }
}

    return JsonResponse(result)

def chart_fold(request):

    result={
            'status':True,
            'data':{
                
            }
        }


    return JsonResponse(result)

# def chart_map(request):

#         return JsonResponse(result)