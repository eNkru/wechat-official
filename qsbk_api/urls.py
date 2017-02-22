from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from qsbk_api import views

urlpatterns = patterns('qsbk_api.views',
                       url(r'^', views.TestView.as_view(), name='test-view'),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)