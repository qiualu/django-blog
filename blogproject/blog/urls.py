from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^25/$',views.index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail')

]



