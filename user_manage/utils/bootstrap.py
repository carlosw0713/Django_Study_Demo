from django import forms

# 公共方法
class BootStrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置

        # self.initial.update(self.Meta.initial)

        for name, field in self.fields.items():
            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label


            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }
#
# modelform
class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass

# form
class BootStrapForm(BootStrap, forms.Form):
    pass