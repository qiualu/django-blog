from django import template
from ..models import Post,Category,Tag
from django.db.models.aggregates import Count

register = template.Library()

# 编写模板标签代码    编写模板标签代码   编写模板标签代码
'''
# 自定义模板标签代码写在 blog_tags.py 文件
# 中。其实模板标签本质上就是一个 Python 函数，因此按照 Python 函数的思路来编
# 写模板标签的代码就可以了
'''   #标签 概述
# 模板标签目录结构 和 使用
'''
# 首先在我们的 blog 应用下创建一个 templatetags 文件夹。然后在这个文件夹下创建
# 一个 __init__.py 文件，使这个文件夹成为一个 Python 包，之后在 templatetags\ 目
# 录下创建一个 blog_tags.py 文件，这个文件存放自定义的模板标签代码。
#
# 这里我们首先导入 template 这个模块，然后实例化了一个 template.Library 类，并将
# 函数 get_recent_posts 装饰为 register.simple_tag。这样就可以在模板中使用语法 {%
# get_recent_posts %} 调用这个函数了（自定义模板标签的步骤）。
'''





# 最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):   #  够通过 {%get_recent_posts %} 的语法在模板中调用这个函数
    return Post.objects.all().order_by('-created_time')[:num]
'''
# 在模板中写入 {% get_recent_posts as
# recent_post_list %}，那么模板中就会有一个从数据库获取的最新文章列表，并通过
# as 语句保存到 recent_post_list 模板变量里。这样我们就可以通过 {% for %} {%
# endfor%} 模板标签来循环这个变量
'''#  #函数作用过程



# 归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')    #order='DESC' 表明降序排列（即离当前越近的时间越排在前面）
# 这里 dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，
# 且是 Python 的 date 对象，精确到月份，降序排列。


# 分类模板标签
@register.simple_tag
def get_categories():
    # return Category.objects.all() # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    #记得在顶部引入Tag models
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)



# 使用自定义的模板标签
'''
我们首先需要在模板中导入存放这些模板标签
的模块，这里是 blog_tags.py 模块。当时我们为了使用 static 模板标签时曾经导入
过 {% load staticfiles %}，这次在 {% load staticfiles %} 下再导入 blog_tags：
{% load blog_tags %}

如:
{% load staticfiles %}
{% load blog_tags %}
<!DOCTYPE html>
<html>
  ...
</html>

使用:
 {% get_recent_posts as recent_post_list %}
 <ul>
 {% for post in recent_post_list %}
 <li>
 <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
 </li>
 {% empty %}
 暂无文章！
 {% endfor %}



'''
