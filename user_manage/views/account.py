#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: account.py
@time: 2023/4/24  13:52
"""
from django import forms

from django.shortcuts import render, redirect,HttpResponse

from  user_manage import  models
from user_manage.utils.bootstrap import BootStrapForm
from user_manage.utils.encrypt import md5
from user_manage.utils.Verifiy_code import check_code


class LoginForm(BootStrapForm):
    pass
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'class':'form-control'}),

        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    # 将输入的密码转化为md5格式
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form=LoginForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data,'填写信息')

        # 验证码的校验
        user_input_code=form.cleaned_data.pop('code')
        code = request.session.get('image_code','')
        # print(user_input_code,code)
        if code.upper() != user_input_code.upper(): # upper()转大写
            form.add_error('code','验证码错误')
            return render(request, 'login.html', {'form': form})

        # 验证成功，获取到的用户名和密码
        # {'name': 'wupeiqi', 'password': '123',"code":123}
        # {'name': 'wupeiqi', 'password': '5e5c3bad7eb35cba3638e145c830c35f',"code":xxx}
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")# 主动往form中添加错误信息
            # form.add_error("name", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.name}
        # session可以保存2小时
        request.session.set_expiry(60 * 60 *2)

        return redirect("/admin/list/")

    return render(request, 'login.html', {'form': form})


def logout(request):
    '''注销'''
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    '''生成图片验证码'''

    # 从内存中读取文件
    from io import BytesIO
    img,code_string=check_code()
    print(img,code_string)

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream=BytesIO()
    img.save(stream,'png')
    # stream.getvalue()

    return HttpResponse(stream.getvalue())



