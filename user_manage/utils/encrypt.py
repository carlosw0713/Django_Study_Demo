#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: encrypt.py
@time: 2023/4/23  17:25
"""
import hashlib

from django.conf import settings

def md5(data_string):

    # 如果不添加 密文 加密就是固定的
    # 调用django中自带的加密密文
    obj=hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()