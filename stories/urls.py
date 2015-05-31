from django.conf.urls import patterns, include, url
from stories import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^write/$', views.StoryChunkCreateView.as_view(), name='write'),
    url(r'^write/(?P<story_pk>\d+)/$', views.StoryChunkCreateView.as_view(), name='write'),
    url(r'^write/(?P<story_pk>\d+)/(?P<pk>\d+)/$', views.StoryChunkUpdateView.as_view(), name='write'),
    url(r'^story/(?P<pk>\d+)/$', views.StoryView.as_view(), name='story'),
)
