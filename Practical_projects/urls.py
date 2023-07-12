"""
URL configuration for Practical_projects project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from user_manage.views import depart,user,admin,account,task,Order,chart,upload

# 添加一个
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings



urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # path('admin/', admin.site.urls),
    path('', depart.depart_list, name='index'),
    path('depart/list/',depart.depart_list),
    path('depart/add/',depart.depart_add),
    path('depart/delete/',depart.depart_delete),

    # 支持xxxx/depart/<int: nid>/edit/ 显示
    path('depart/<int:nid>/edit/', depart.depart_edit),
    # path('/<int:nid>/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list,name='user_list_redirect'),
    path('user/add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/delete/',user.user_delete),

    # 管理员
    path('admin/list/',admin.admin_list),
    path('admin/add/',admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 任务管理

    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),
    path('task/add/', task.task_add),


    # 订单管理
    path('Order/list/', Order.Order_list),
    path('Order/add/', Order.Order_add),
    path('Order/delete/', Order.Order_delete),
    path('Order/detail/', Order.Order_detail),
    path('Order/edit/', Order.Order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/fold/', chart.chart_fold),
    # path('chart/map/', chart.chart_map),


    # 文件上传
    path('upload/list/', upload.upload_list),
    path('upload/multi/', upload.upload_multi),
    path('upload/form/', upload.upload_form),

    path('upload/model_form/add/', upload.upload_model_form_add),
    path('upload/model_form/list/', upload.upload_model_form_list),

    





]
