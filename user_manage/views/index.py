#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:carlos
@file: index.py
@time: 2023/4/23  13:39
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