from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

# regular expression   re正则简写
app_name = 'blog'  #' 告诉 Django 这个 urls.py 模块是属于 blog 应用的  这种技术叫做视图函数命名空间

'''
# 在 Django 中 URL 模式的
# 配置方式就是通过 url 函数将 URL 和视图函数绑定。比如 url(r'^$', views.index,
# name='index')，它的第一个参数是 URL 模式，第二个参数是视图函数 index。
# 对 url 函数 来说，第二个参数传入的值必须是一个函数
'''  # url 函数

urlpatterns = [
    # url(r'^$',views.index,name='index'),  #普通视图
    url(r'^$',views.IndexView.as_view(),name='index'),  #类视图
    #将类视图转换成函数视图非常简单，只需调用类视图的 as_view() 方法即可

    # 访问 /archives/2017/3/，那么 archives 视图函
    # 数的实际调用为：archives(request, year=2017, month=3)。
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives,name='archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),

    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),

    # url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),  # post/1
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),  # post/1

    # 标签视图函数
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),


]