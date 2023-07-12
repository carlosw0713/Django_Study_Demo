from django.db import models

# Create your models here.

from django.db import models

'''
python manage.py makemigrations
python manage.py makemigrations
'''



from django.db import models


class Picture(models.Model):
    """ 图片 """
    name = models.CharField(verbose_name="名称", max_length=32)
    type = models.CharField(verbose_name="类型" ,max_length=32)

    # 本质上数据库也是CharField，自动保存数据。 upload_to 指定上传到media的某个目录
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='Picture/')



class performance(models.Model):
    """业绩表"""
    depart = models.CharField(verbose_name="部门名称", max_length=32)
    sales = models.IntegerField(verbose_name="销售额")
    file = models.CharField(verbose_name="部门文件", max_length=128)

    class Meta:
        verbose_name = "业绩表"
        verbose_name_plural = "业绩表"

    '''
    verbose_name：用于设置模型的单数名称，即在后台管理界面显示该模型记录时的名称。例如，
    若将 verbose_name 设置为 "业绩表"，则在后台管理界面中，该模型记录的每一个实例会以 
    "业绩表" 的名称进行展示。verbose_name_plural：用于设置模型的复数名称，即在后台管理界
    面中显示多个该模型记录时的名称。如果未设置该属性，系统会默认将 verbose_name 加上 "s" 
    后作为复数名称。例如，若将 verbose_name 设置为 "业绩表"，则 verbose_name_plural 会
    自动设置为 "业绩表s"
    '''



class Order(models.Model):
    '''订单管理'''

    oid=models.CharField(verbose_name='订单号',max_length=64)
    title = models.CharField(verbose_name='名称', max_length=64,unique=True)
    price = models.IntegerField(verbose_name='价格',)

    status_choices=(
        (1,"待支付"),
        (2,"已支付"),
    )
    status=models.SmallIntegerField(verbose_name='状态',choices=status_choices,default=1)
    username = models.ForeignKey(verbose_name='购买用户',to="Admin",on_delete=models.CASCADE,default=2)

class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Admin(models.Model):
    '''管理员'''
    name = models.CharField(verbose_name='姓名', max_length=32,unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)

    # 面对对象 将 实例化对象 输出 title的内容
    def __str__(self):
        return self.name

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)


    # 面对对象 将 实例化对象 输出 title的内容
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """ 员工表 """
    # unique = True 名字设置为唯一值
    name = models.CharField(verbose_name="姓名", max_length=64,null=False,unique=True)
    password = models.CharField(verbose_name="密码", max_length=64,null=True,blank=True)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间",null=True,blank=True)

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束
    #   - to，与那张表关联
    #   - to_field，表中的那一列关联
    # 2.django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.部门表被删除
    # ### 3.1 级联删除 数据库索引

    # blank = True blank=False 表示该字段不允许为空字符串。 ,null=True 字段是为非必填字段
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE,blank=True,null=True)
    # ### 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )

    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices,blank=False)
