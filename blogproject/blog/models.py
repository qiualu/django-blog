from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from markdown import Markdown
import markdown
from django.utils.html import strip_tags




# 标签数据库表
class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


# 分类数据库表
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



# 文章（Post）
@python_2_unicode_compatible    # ??????
class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)

    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用TextField来存储大段文本。
    # 文章正文，我们使用了 TextField。注意不需要加参数
    body = models.TextField()

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用DateTimeField类型。
    created_time = models.DateTimeField(auto_now_add=True)   #自动赋值不能修改
    modified_time = models.DateTimeField(auto_now=True) #default=timezone.now修改时自动赋值能修改（auto_now_add不能修改）

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)


    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用ManyToManyField，表明这是多对多的关联关系
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships

    #  分类          一对多的关联关系  关联对象
    category = models.ForeignKey(Category)
    #  标签         多对多的关联关系
    tags = models.ManyToManyField(Tag, blank=True)

    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和Category类似。
    #  作者          一对多的关联关系/关联对象
    author = models.ForeignKey(User)


    def get_absolute_url(self):
        # 使用reverse函数，生成一个url，例如 post / 1
        return reverse('blog:detail', kwargs={'pk': self.pk})  #



    class Meta:
        ordering = ['-created_time']  #ordering 属性用来指定文章排序方式  ['-created_time'] 指定了依据哪个属性的值进行排序
        # 负号表示逆序排列。列表中可以用多个 项，比如ordering = ['-created_time', 'title']

    # 新增 views 字段记录阅读量
    views = models.PositiveIntegerField(default=0)
    # 一旦用户访问了某篇文章，这时就应该将views的值 + 1，这个过程最好由 Post模型自
    # 己来完成，因此再给模型添加一个自定义的方法：

    def increase_views(self):   #只需在视图函数中调用模型的 increase_views 方法即可。
        self.views += 1
        self.save(update_fields=['views'])

    # def save(self, *args, **kwargs):
    #     # 如果没有填写摘要
    #     if not self.excerpt:
    #         # 首先实例化一个 Markdown 类，用于渲染 body 的文本
    #         md = markdown.Markdown(extensions=[
    #             'markdown.extensions.extra',
    #             'markdown.extensions.codehilite',
    #         ])  # 先将 Markdown 文本渲染成 HTML 文本
    #
    #         # strip_tags 去掉 HTML 文本的全部 HTML 标签
    #         # 从文本摘取前 54 个字符赋给 excerpt
    #         self.excerpt = strip_tags(md.convert(self.body))[:54]
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):  #创建数据库存储时调用
        if not self.excerpt:
            md = Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:32]
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title