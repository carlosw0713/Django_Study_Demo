from user_manage.models import UserInfo
from user_manage import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from user_manage.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator


from django import forms




class UserModelForm_add(BootStrapModelForm):

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

        # 修改字段占位符属性
        self.fields['name'].widget.attrs['placeholder'] = '请输入名称'

        self.fields['age'].widget.attrs['placeholder'] = '请选择'
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



class UserModelForm_edit(BootStrapModelForm):

    # # init 对原来已有的方法重新定义新内容 比如添加class属性。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    #  Django 3.2 版本之后，regex 参数已被弃用，并已从 Django 表单中删除
    from django.core.validators import RegexValidator
    # password = forms.CharField(validators=[RegexValidator(r'^\d{6}$', message='直接调用form方法，请输入6位数字')])

    # create_time = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
    #     label='入职日期',
    #     required = False  # 添加此参数以将字段设置为非必填
    # )