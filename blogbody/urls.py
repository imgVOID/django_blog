from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^archieve$', views.archieve, name='archieve'),
]
