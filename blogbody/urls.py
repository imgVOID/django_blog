from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.tag_detail, name='tag_detail'),
    url(r'^archieve$', views.archieve, name='archieve'),
    url(r'^search$', views.search, name="search"),
    url(r'^tags$', views.tags_list, name="tags_list")
]
