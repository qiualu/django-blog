from django.db import models

# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=100)   #评论用户的 name（名字）、
    email = models.EmailField(max_length=255) #评论用户的 email（邮箱）
    url = models.URLField(blank=True)         #评论用户的 url（个人网站）
    text = models.TextField()     # 用户发表的 内容将存放在 text 字段里
    created_time = models.DateTimeField(auto_now_add=True) #记录用户发表评论的时间  自动添加
    post = models.ForeignKey('blog.Post')       #关联到某篇文章（Post）

    def __str__(self):
        return self.text[:20]