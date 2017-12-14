from django import forms
from .models import Comment

# Django 的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类。
class CommentForm(forms.ModelForm):  #如果表单对应有一个数据库模型（例如这里的评论表单对应着评论模型），那么使用 ModelForm 类会简单很多
    class Meta:   #表单的内部类 Meta 里指定一些和表单相关的东西。
        model = Comment  #model = Comment 表明这个表单对应的数据库模型是 Comment 类。

        # 指定了表单需要显示的字段，这里我们指定了name、email、url、text需要显示。
        fields = ['name', 'email', 'url', 'text']
# 关于表单进一步的解释
'''
# Django 的表单和这个思想类似（相当于 ORM 思想，不需要手写前端代码）
# 写一个 CommentForm 这个 Python 类。通过调用这个类的一些方法和属性，
# Django 将自动为我们创建常规的表单代码
'''





