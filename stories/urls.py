from django.conf.urls import patterns, include, url
from stories import views

urlpatterns = patterns(
    '',
    url(r'^dash/$', views.dash, name='dash'),
    url(r'^story/(?P<pk>\d+)/$', views.StoryView.as_view(), name='story'),
    url(r'^chunk/(?P<story_pk>\d+)/$', views.StoryChunkCreateView.as_view(), name='chunk'),
    url(r'^chunk/(?P<story_pk>\d+)/(?P<pk>\d+)/$', views.StoryChunkUpdateView.as_view(), name='chunk'),
)
