from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
from django.views.generic import ListView,DetailView
import markdown
from comments.forms import CommentForm

'''
# def index(request):
#     post_list = Post.objects.all()  #  Post.objects.all() 从数据库中获取文章（Post）列表数据，并将其保存到 post_list 变量中。
#     return render(request,'blog/index.html',context={'post_list':post_list,})
'''  # 将 index 视图函数改写为类视图
'''
# index 视图函数首先通过 Post.objects.all() 从数据库中获取文章（Post）列表数据，
# 并将其保存到 post_list 变量中。而在类视图中这个过程 ListView 已经帮我们做了。
# 我们只需告诉 ListView 去数据库获取的模型是 Post，而不是 Comment 或者其它什
# 么模型，即指定 model = Post。将获得的模型数据列表保存到 post_list 里，即指
# 定 context_object_name = 'post_list'。然后渲染 blog/index.html 模板文件，index 视
# 图函数中使用 render 函数。但这个过程 ListView 已经帮我们做了，我们只需指定
# 渲染哪个模板即可。

'''  #IndexView
class IndexView(ListView): #   类视图
    model = Post   #model：将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
    template_name = 'blog/index.html'  #template_name：指定这个视图渲染的模板。
    context_object_name = 'post_list' # 这个name不能瞎取，必须和模板中的变量一直 context_object_name：指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。

    # 类视图ListView已经帮我们写好了上述的分页逻辑，我们只需通过指定paginate_by属性来开启分页功能即可，
    # 即在类视图中指定paginate_by属性的值：
    paginate_by = 2   # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章

    # Pagination 完善分页
    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，

        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。

        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')  #paginator ，即 Paginator 的实例。
        page = context.get('page_obj')  #page_obj ，当前请求页面分页对象。
        is_paginated = context.get('is_paginated')  #is_paginated，是否已分页。只有当分页后页面超过两页时才算已分页。

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)
        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        left = []  # 当前页左边连续的页码号，初始值为空
        right = []   # 当前页右边连续的页码号，初始值为空

        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        first = False   # 初始值为 False
        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:  #??????????????????????????????????????????????????????????????????????????????
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。切片时如果溢出自动截断
            right = page_range[page_number:page_number + 2] #获取了当前页码后连续两个页码
            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True
                # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码

                # ??????????????????????????????????????????????????????????????????????????????
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True
            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data






'''  # category 视图函数的功能也是从数据库中获取文章列表数据
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
'''  # category 视图函数的功能也是从数据库中获取文章列表数据
class CategoryView(IndexView):  # ListView -> IndexView继承
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'
    #
    '''
    # 覆写了父类的 get_queryset 方法。该方法默认获
    # 取指定模型的全部列表数据。为了获取指定分类下的文章列表数据，我们覆写该
    # 方法，改变它的默认行为。
    # 从URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，非命名组
    # 参数值保存在实例的 args 属性（是一个列表）里。
    # self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值。
    # 调用父类的 get_queryset 方法获得全部文章列表
    #
    '''
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk')) #从URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里
        return super(CategoryView, self).get_queryset().filter(category=cate)


'''  #archives 视图函数
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,  #使用 filter 来根据条件过滤
                                    created_time__month=month,
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
'''  #archives 视图函数
'''
用模型管理器（objects）的 filter 函数来过滤文章。
根据 created_time 的 year 和 month 属性过滤，筛选出文章发表在对应的 year 年和
month 月的文章。注意这里 created_time 是 Python 的 date 对象，其有一个 year 和 month 属性，我们在上一章使用过这个属性。
Python 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表，所以 Django 要
求我们把点替换成了****两个下划线****，即 created_time__year。同时和 index 视图中一样，
我们对返回的文章列表进行了排序。此外由于归档的下的文章列表的显示和首页是一
样的，因此我们直接渲染了 index.html 模板。

''' # 函数详解
class ArchivesView(IndexView):
    def get_queryset(self):
        return super(ArchivesView,self).get_queryset().filter(
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
        )

'''
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)# 从django.shortcuts 模块导入的 get_object_or_404 方法
    # 其作用就是当传入的 pk 对应的Post 在数据库存在时，就返回对应的 post，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。

    post.increase_views() # 阅读量 +1

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',  #codehilite 是语法高亮拓展
                                      'markdown.extensions.toc',   # toc 则允许我们自动生成目录
                                  ])
    # 记得在顶部导入 CommentForm，这里实例化没有 request.POST 作为参数，因此表单都是空的
    form = CommentForm()

    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,   # 文章
               'form': form,   # 表单
               'comment_list': comment_list  # 评论
               }

    return render(request, 'blog/detail.html', context=context)
'''  #  detail(request, pk)
'''
#    用 Markdown 语法写的测试
#    # 一级标题
#    ## 二级标题
#    ### 三级标题
#    >引用
#    - 无序列表
#    - 无序列表
#    - 无序列表
#    [百度的链接](http://baidu.com)
#    ![图片](http://box.bdimg.com/static/fisp_static/common/img/searchbox/logo_news_276_88_1f9876a.png)
#    ```python
#    def detail(request, pk):
#        post = get_object_or_404(Post, pk=pk)
#        post.body = markdown.markdown(post.body,extensions=[
#                                                'markdown.extensions.extra',
#                                                'markdown.extensions.codehilite',
#                                                'markdown.extensions.toc',])
#    return render(request, 'blog/detail.html', context={'post':post})
#    ```

'''    #Markdown 语法
'''
# 任何的 HTML 代码在 Django 的模板中都会被转义（即显示原始的 HTML 代
# 码，而不是经浏览器渲染后的格式）。为了解除转义，只需在模板标签使用 safe 过滤
# 器即可，告诉 Django，这段文本是安全的，你什么也不用做。在模板中找到展示博
# 客文章主体的 {{ post.body }} 部分，为其加上 safe 过滤器，{{ post.body|safe }}，
# 大功告成，这下看到预期效果了。
#
# safe 过滤器，{{ post.body|safe }}，
#
# safe 是 Django 模板系统中的过滤器（Filter），可以简单地把它看成是一种函数，其
# 作用是作用于模板变量，将模板变量的值变为经过滤器处理过后的值。例如这里
# {{ post.body|safe }}，本来 {{ post.body }} 经模板系统渲染后应该显示 body 本身的
# 值，但是在后面加上 safe 过滤器后，渲染的值不再是 body 本身的值，而是由 safe
# 函数处理后返回的值。过滤器的用法是在模板变量后加一个 | 管道符号，再加上过滤
# 器的名称。可以连续使用多个过滤器，例如 {{ var|filter1|filter2 }}。
'''   #safe 标签   转义html
# PostDetailView 稍微复杂一点，主要是等价的 detail 视图函数
class PostDetailView(DetailView):  #  Django 提供了一个 DetailView 类视图
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    #get 方法。这对应着 detail 视图函数中将 post 的阅读量 +1 的那部分代码。事实上，你可以简单地把get 方法的调用看成是 detail 视图函数的调用
    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse 对象
        return response

    #
    def get_object(self, queryset=None):
        # # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        # post = super(PostDetailView, self).get_object(queryset=None)   # ????????????
        # post.body = markdown.markdown(post.body,
        #                               extensions=[
        #                                   'markdown.extensions.extra',
        #                                   'markdown.extensions.codehilite',
        #                                   'markdown.extensions.toc',
        #                               ])
        # # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    # get_context_data方法。这部分对应着detail视图函数中生成评论表
    # 单、获取post下的评论列表的代码部分。这个方法返回的值是一个字典，这个字典就是模板变量字典，最终会被传递给模板。
    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。也就是往 context 里添加内容
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context

# 类视图
# ???
# ???
# ???

# 标签视图函数
class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)






