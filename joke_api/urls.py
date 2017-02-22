from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from joke_api import views

urlpatterns = patterns('joke_api.views',
                       url(r'^', views.modes),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
