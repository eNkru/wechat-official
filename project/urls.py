from django.conf.urls import include, url
from django.contrib import admin
from werobot.contrib.django import make_view
from we_robot.robot import robot
from welcome.views import index, health
from post_api import post_engine
from tuling import tuling_robot

urlpatterns = [
    url(r'^$', index),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^qsbk/$', include('qsbk_api.urls')),
    url(r'^joke/$', include('joke_api.urls')),
    url(r'^robot/', make_view(robot)),
    url(r'^tuling$', tuling_robot.tuling_api),
    url(r'^post/(?P<pk>[a-zA-Z0-9]+)$', post_engine.get_post_details),
]
