from django.core.exceptions import ValidationError
from django.forms import forms
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from user_manage import models
from django.core.paginator import Paginator



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


############################# ModelFrom 示例 ####################################
from django import  forms
from .models import UserInfo
#  Django 3.2 版本之后，regex 参数已被弃用，并已从 Django 表单中删除
from django.core.validators import RegexValidator

class UserModelForm_add(forms.ModelForm):

    '''直接添加字段校验规格 点击查看详细表单操作信息'''
    '''max_length: 限制输入字符串的最大长度，示例: forms.CharField(max_length=20, label="密码")。
min_length: 限制输入字符串的最小长度，示例: forms.CharField(min_length=6, label="密码")。
required: 定义字段是否为必填项，若为 True，则不能为空，示例: forms.CharField(required=True, label="邮箱")。
regex: 用正则表达式匹配输入内容，示例: forms.CharField(regex=r'[0-9]+', label="验证码")。
widget: 定义表单控件，如下拉框、日期选择器等，示例: forms.Select(choices=gender_choices, label="性别")。
initial: 定义初始值，示例: forms.CharField(initial="hello", label="问候语")。
label: 定义标签，即该字段在表单中的显示名称，示例: forms.CharField(label="昵称")。
help_text: 定义帮助文本，即表单控件下方的提示信息，示例: forms.CharField(help_text="请输入您的身份证号码", label="身份证号")。
error_messages: 定义错误信息，即在校验失败时返回的错误提示，示例: forms.EmailField(error_messages={'invalid': '请输入正确的邮箱地址'}, label="邮箱")。
validators: 定义自定义的验证器，用于对输入内容进行更加细致的校验，示例: forms.CharField(validators=[custom_validator], label="考试成绩")。'''
    name = forms.CharField(min_length=3,max_length=10,label="用户名",)
    # name= forms.EmailField(error_messages={'invalid': '请输入姓名'})

    account=forms.CharField(initial="520.12",label='余额')

    # 使用自带的时间控件
    # create_time = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
    #     label='入职日期',
    #     required=False  # 添加此参数以将字段设置为非必填
    # )
    # 调用js和css组件 暂时不行
    # create_time=forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datepicker'}))

    # init 对原来已有的方法重新定义新内容 比如添加class属性。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 为字段添加 class 属性
        # 传统一个一个添加表单样式
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            # 修改字段占位符属性
            self.fields['name'].widget.attrs['placeholder'] = '请输入名称'

            self.fields['gender'].widget.attrs['placeholder'] = '请选择'
            self.fields['depart'].widget.attrs['placeholder'] = '请选择'


    class Meta:
        # 直接获取 models.UserInfo 的实例对象
        model=UserInfo
        # 取表单实例中的可能运用到的值 其中“depart”就是表单中定义的内容 并且返回信息 通过 __str__方法设置返回
        # fields = ["name", "age", 'account', 'create_time', "gender", "depart"]
        # 所有字段
        # fields='__all__'
        # 不包含什么字段
        exclude = ['id', 'password']



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



class UserModelForm_edit(forms.ModelForm):

    # init 对原来已有的方法重新定义新内容 比如添加class属性。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            # 修改字段占位符属性
            self.fields['name'].widget.attrs['placeholder'] = '请输入名称'

            self.fields['name'].error_messages = {
                'unique': '该名称重复，请重新填写并上传名称'
            }
            self.fields['depart'].widget.attrs['placeholder'] = '请选择'

    class Meta:
        # 直接获取 models.UserInfo 的实例对象
        model=UserInfo
        # 取表单实例中的可能运用到的值 其中“depart”就是表单中定义的内容 并且返回信息 通过 __str__方法设置返回
        fields = ["name","age",'password', 'create_time', "depart"]


    # 方式 1.创建钩子函数去校验 常用于校验长度是否刚好 还需要去调用
    def password_6(self):

        # 暂时有点问题
        pwd=self.cleaned_data['password']
        if len(pwd)!=6:
            # 验证不通过
            raise ValidationError('创建钩子函数，密码只能为6位')

        # 验证通过，用户值返回
        return pwd
    # 方式2 校验数据格式可以直接通过forms校验
    # password = forms.CharField(validators=[RegexValidator(r'^\d{6}$', message='直接调用form方法，请输入6位数字')])

    # create_time = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
    #     label='入职日期',
    #     required = False  # 添加此参数以将字段设置为非必填
    # )


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



