from django.conf.urls import patterns, include, url

from main.views import ImageListView, ImageDetailView, ImageCreateView, ImageDeleteView, UserView, TagView
from main.feeds import IndexFeed, UserFeed, TagFeed

urlpatterns = patterns('',               
    url(r'^$', ImageListView.as_view(), name='index'),
    url(r'^(?i)page/(?P<page>\d+)$', ImageListView.as_view(), name='index_page'),
    
    url(r'^(?i)image/(?P<pk>\d+)$', ImageDetailView.as_view(), name='image'),
    url(r'^(?i)image/(?P<pk>\d+)/delete$', ImageDeleteView.as_view(), name='image_delete'),
    
    url(r'^(?i)upload', ImageCreateView.as_view(), name='upload'),
    
    url(r'^(?i)user/(?P<user>[\w.@+-]+)$', UserView.as_view(), name='user'),
    url(r'^(?i)user/(?P<user>[\w.@+-]+)/page/(?P<page>\d+)$', UserView.as_view(), name='user_page'),
    
    url(r'^(?i)tag/(?P<tag>\w+)$', TagView.as_view(), name='tag'),
    url(r'^(?i)tag/(?P<tag>\w+)/page/(?P<page>\d+)$', TagView.as_view(), name='tag_page'),
    
    url(r'^(?i)feed$', IndexFeed(), name='index_feed'),
    url(r'^(?i)feed/user/(?P<user>[\w.@+-]+)$', UserFeed(), name='user_feed'),
    url(r'^(?i)feed/tag/(?P<tag>\w+)$', TagFeed(), name='tag_feed'),
)